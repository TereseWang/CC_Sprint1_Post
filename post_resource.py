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

        conn = PostResource._get_connection()
        cur = conn.cursor()
        if key == "all":
            sql = "SELECT * FROM f22_cc_databases.post_table"
            res = cur.execute(sql)
            # ToDo: fetchmany() can be used when pagination
            result = cur.fetchall()
        else:
            sql = "SELECT * FROM f22_cc_databases.post_table where postId=%d"
            res = cur.execute(sql, args=key)
            result = cur.fetchone()

        return result

    @staticmethod
    def create_by_user(uid, post_content):
        pid = random.randint(0, 10000000000)
        insert_sql = """
            insert into f22_cc_databases.post_table(postId, userId, post)
            values(%d,%d,%s)
        """

        result = None
        try:
            conn = PostResource._get_connection()
            cur = conn.cursor()
            res = cur.execute(insert_sql, args=[pid, uid, post_content])
            result = PostResource.get_by_key(pid)
        except Exception as e:
            print("Exception: ", e)

        return result

    @staticmethod
    def delete_by_key(pid):
        delete_sql = """
            DELETE FROM f22_cc_databases.post_table WHERE postId=%d
        """

        result = None
        try:
            conn = PostResource._get_connection()
            cur = conn.cursor()
            res = cur.execute(delete_sql, args=pid)
            result = PostResource.get_by_key(pid)
        except Exception as e:
            print("Exception: ", e)

        return result

    @staticmethod
    def update_by_key(pid, content):
        update_sql = """
                UPDATE f22_cc_databases.post_table 
                SET post=%s
                WHERE postId=%d
            """
        result = None
        try:
            conn = PostResource._get_connection()
            cur = conn.cursor()
            res = cur.execute(update_sql, args=[content, pid])
            result = PostResource.get_by_key(pid)
        except Exception as e:
            print("Exception: ", e)

        return result
