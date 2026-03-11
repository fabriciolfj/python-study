import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

# -------------------------------------------------------------------
# Configuração do cliente (ajuste region/endpoint conforme ambiente)
# -------------------------------------------------------------------
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    # endpoint_url="http://localhost:4566",  # LocalStack
)

TABLE_NAME = "produtos"
table = dynamodb.Table(TABLE_NAME)


# -------------------------------------------------------------------
# INSERT – put_item
# -------------------------------------------------------------------
def inserir_produto(product_id: str, name: str, price: float, store: int, create_date: str) -> None:
    try:
        table.put_item(
            Item={
                "produto_id": product_id,
                "criado_em": create_date,
                "nome": name,
                "preco": Decimal(str(price)),
                "estoque": store,
            }
        )

        print(f"[INSERT] Product '{product_id}' criado com sucesso.")
    except ClientError as e:
        print(f"[ERRO] {e.response['Error']['Message']}")


# -------------------------------------------------------------------
# GET – get_item (busca pela PK)
# -------------------------------------------------------------------
def buscar_produto(produto_id: str, criado_em: str) -> dict | None:
    try:
        response = table.get_item(Key={"produto_id": produto_id, "criado_em": criado_em})
        item = response.get("item")
        if item:
            print(f"[GET] Encontrado: {item}")
        else:
            print(f"[GET] Produto '{produto_id}' não encontrado.")
        return item
    except ClientError as e:
        print(f"[ERRO] {e.response['Error']['Message']}")
        return None


# -------------------------------------------------------------------
# QUERY – busca por PK + range na SK (criado_em)
# -------------------------------------------------------------------
def listar_produtos_por_periodo(produto_id: str, inicio: str, fim: str) -> list:
    """Retorna todos os itens de uma PK dentro do intervalo de SK informado."""
    try:
        response = table.query(
            KeyConditionExpression=(
                Key("produto_id").eq(produto_id)
                & Key("criado_em").between(inicio, fim)
            )
        )
        items = response.get("Items", [])
        print(f"[QUERY] {len(items)} item(s) encontrado(s): {items}")
        return items
    except ClientError as e:
        print(f"[ERRO] {e.response['Error']['Message']}")
        return []


# -------------------------------------------------------------------
# UPDATE – update_item
# -------------------------------------------------------------------
def atualizar_estoque(produto_id: str, criado_em: str, novo_estoque: int) -> None:
    try:
        table.update_item(
            Key={"produto_id": produto_id, "criado_em": criado_em},
            UpdateExpression="SET estoque = :val",
            ExpressionAttributeValues={":val": novo_estoque},
        )
        print(f"[UPDATE] Estoque do produto '{produto_id}' atualizado para {novo_estoque}.")
    except ClientError as e:
        print(f"[ERRO] {e.response['Error']['Message']}")


# -------------------------------------------------------------------
# DELETE – delete_item
# -------------------------------------------------------------------
def deletar_produto(produto_id: str, criado_em: str) -> None:
    try:
        table.delete_item(Key={"produto_id": produto_id, "criado_em": criado_em})
        print(f"[DELETE] Produto '{produto_id}' removido.")
    except ClientError as e:
        print(f"[ERRO] {e.response['Error']['Message']}")


# -------------------------------------------------------------------
# Demo
# -------------------------------------------------------------------
if __name__ == "__main__":
    inserir_produto("P001", "Teclado Mecânico", 349.90, 50, "2024-01-10T10:00:00")
    inserir_produto("P001", "Teclado Mecânico PRO", 499.90, 20, "2024-06-15T14:30:00")
    inserir_produto("P002", "Mouse Gamer", 199.90, 120, "2024-03-01T09:00:00")

    buscar_produto("P001", "2024-01-10T10:00:00")
    buscar_produto("P999", "2024-01-01T00:00:00")   # não existe

    # Query: todos os itens de P001 no primeiro semestre de 2024
    listar_produtos_por_periodo("P001", "2024-01-01T00:00:00", "2024-06-30T23:59:59")

    atualizar_estoque("P001", "2024-01-10T10:00:00", 45)
    buscar_produto("P001", "2024-01-10T10:00:00")   # valida update

    deletar_produto("P002", "2024-03-01T09:00:00")
    buscar_produto("P002", "2024-03-01T09:00:00")   # confirma remoção