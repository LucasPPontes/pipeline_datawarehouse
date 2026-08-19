from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import require_roles
from app.audit import registrar_auditoria
from app.models.vendas import ClienteVenda, ProdutoVenda, PedidoVenda, ItemPedidoVenda
from app.schemas.vendas import (
    ClienteVendaCreate, ClienteVendaResponse,
    ProdutoVendaCreate, ProdutoVendaResponse,
    PedidoVendaCreate, PedidoVendaResponse,
    ItemPedidoVendaCreate, ItemPedidoVendaResponse,
)

router = APIRouter(
    prefix="/vendas",
    tags=["Vendas"],
    dependencies=[Depends(require_roles(["VENDAS"]))]
)

# 1. Clientes
@router.get("/clientes", response_model=List[ClienteVendaResponse], summary="Listar clientes de vendas")
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(ClienteVenda).all()

@router.get("/clientes/{cliente_id}", response_model=ClienteVendaResponse, summary="Obter cliente por ID")
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteVenda).filter(ClienteVenda.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/clientes", response_model=ClienteVendaResponse, status_code=201, summary="Cadastrar cliente")
def criar_cliente(request: Request, cliente: ClienteVendaCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["VENDAS"]))):
    novo_cliente = ClienteVenda(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    registrar_auditoria(db, current_user.email, "CRIAR_CLIENTE_VENDA", "/vendas/clientes", "POST", request.client.host if request.client else "127.0.0.1")
    return novo_cliente

# 2. Produtos
@router.get("/produtos", response_model=List[ProdutoVendaResponse], summary="Listar produtos do catálogo")
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoVenda).all()

@router.get("/produtos/{produto_id}", response_model=ProdutoVendaResponse, summary="Obter produto por ID")
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    prod = db.query(ProdutoVenda).filter(ProdutoVenda.id == produto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return prod

@router.post("/produtos", response_model=ProdutoVendaResponse, status_code=201, summary="Cadastrar produto")
def criar_produto(request: Request, produto: ProdutoVendaCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["VENDAS"]))):
    novo_prod = ProdutoVenda(**produto.model_dump())
    db.add(novo_prod)
    db.commit()
    db.refresh(novo_prod)
    registrar_auditoria(db, current_user.email, "CRIAR_PRODUTO_VENDA", "/vendas/produtos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo_prod

# 3. Pedidos
@router.get("/pedidos", response_model=List[PedidoVendaResponse], summary="Listar pedidos de vendas")
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(PedidoVenda).all()

@router.get("/pedidos/{pedido_id}", response_model=PedidoVendaResponse, summary="Obter pedido por ID")
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoVenda).filter(PedidoVenda.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.post("/pedidos", response_model=PedidoVendaResponse, status_code=201, summary="Criar pedido de venda")
def criar_pedido(request: Request, pedido: PedidoVendaCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["VENDAS"]))):
    novo_pedido = PedidoVenda(**pedido.model_dump())
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    registrar_auditoria(db, current_user.email, "CRIAR_PEDIDO_VENDA", "/vendas/pedidos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo_pedido

# 4. Itens do Pedido
@router.get("/itens-pedido", response_model=List[ItemPedidoVendaResponse], summary="Listar itens dos pedidos")
def listar_itens_pedido(db: Session = Depends(get_db)):
    return db.query(ItemPedidoVenda).all()

@router.post("/itens-pedido", response_model=ItemPedidoVendaResponse, status_code=201, summary="Adicionar item ao pedido")
def criar_item_pedido(request: Request, item: ItemPedidoVendaCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["VENDAS"]))):
    novo_item = ItemPedidoVenda(**item.model_dump())
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    registrar_auditoria(db, current_user.email, "CRIAR_ITEM_PEDIDO_VENDA", "/vendas/itens-pedido", "POST", request.client.host if request.client else "127.0.0.1")
    return novo_item
