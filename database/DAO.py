from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getStores():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from stores"""

        cursor.execute(query)

        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getAllNodes(store_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders
                    where store_id = %s"""

        cursor.execute(query, (store_id,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(store_id, nGiorniMax):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT o1.order_id AS o1, o2.order_id AS o2, sum(oi1.quantity)+sum(oi2.quantity) as weight
                    FROM orders o1, orders o2, order_items oi1, order_items oi2
                    WHERE oi1.order_id = o1.order_id
                    and oi2.order_id = o2.order_id 
                    and o1.store_id = %s 
                      AND o2.store_id = %s
                      AND o1.order_id != o2.order_id
                      AND o1.order_date > o2.order_date
                      AND DATEDIFF(o1.order_date, o2.order_date) < %s
                    group by o1.order_id, o2.order_id """

        cursor.execute(query, (store_id, store_id, nGiorniMax))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result
