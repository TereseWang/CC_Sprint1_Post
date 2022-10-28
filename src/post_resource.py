import pymysql
import random
import os


class PostResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def get_by_key(key):

        sql = "SELECT * FROM f22_cc_databases.post_table where pid=%s";
        conn = PostResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql, args=key)
        result = cur.fetchone()

        return result

    @staticmethod
    def create_by_user(uid, post_content):
        pid = random.randint(10000)
        insert_sql = """
            insert into f22_cc_databases.post_table(pid, uid, post)
            values(%s,%s,%s)
        """

        # sql = "SELECT * FROM f22_cc_databases.post_table where pid=%s";
        conn = PostResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(insert_sql, args=[pid, uid, post_content])
        result = cur.fetchone()

        return result