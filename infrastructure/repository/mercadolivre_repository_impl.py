from application.domain.entitie.mercadolivre_entity import MercadolivreEntity
from application.domain.port.mercadolivre_repository_port import MercadolivreRepository
from infrastructure.persistence.connection import get_connection

class MercadolivreRepositoryImpl(MercadolivreRepository):

    def find_all_product_ids(self) -> list[str]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM mercadolivre")
        rows = cursor.fetchall()

        conn.close()
        return [row[0] for row in rows]

    def save_all(self, affiliates: list[MercadolivreEntity]) -> None:
        if not affiliates:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.executemany(
            """
            INSERT OR REPLACE INTO mercadolivre (id, affiliate_link)
            VALUES (?, ?)
            """,
            [(a.id, a.affiliate_link) for a in affiliates]
        )

        conn.commit()
        conn.close()

    def save(self, affiliate: MercadolivreEntity) -> None:
        conn = get_connection()
        conn.execute(
            "INSERT OR REPLACE INTO mercadolivre (id, affiliate_link) VALUES (?, ?)",
            (affiliate.id, affiliate.affiliate_link)
        )
        conn.commit()
        conn.close()

    def exists_by_product_id(self, product_id: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM mercadolivre WHERE id = ? LIMIT 1",
            (product_id,)
        )

        return cursor.fetchone() is not None

    def find_by_id(self, affiliate_id: str) -> MercadolivreEntity | None:
        conn = get_connection()
        cursor = conn.execute(
            "SELECT id, mercadolivre FROM affiliates WHERE id = ?",
            (affiliate_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row:
            return MercadolivreEntity(id=row[0], affiliate_link=row[1])
        return None
