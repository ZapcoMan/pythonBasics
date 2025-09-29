import pymysql
import logging
import configparser

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='log.log',
                    filemode='a',
                    encoding='utf-8')  # 确保日志文件以UTF-8编码保存

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    提供与数据库交互的方法的类。

    通过读取配置文件来初始化数据库连接信息，并提供连接数据库、执行查询、更新、删除和插入操作的方法。
    """
    def __init__(self, config_file='db_config.ini'):
        """
        初始化数据库连接信息。

        通过读取配置文件来设置数据库的主机、用户、密码、数据库名和端口。
        """
        config = configparser.ConfigParser()
        config.read(config_file)

        self.host = config.get('database', 'host')
        self.user = config.get('database', 'user')
        self.password = config.get('database', 'password')
        self.db = config.get('database', 'db')
        # 添加对端口号的读取
        self.port = config.getint('database', 'port')  # 使用getint来确保读取的是整数

        self.connection = None

    def connect(self):
        """
        建立与数据库的连接。

        如果当前没有活动的连接，尝试根据配置信息连接数据库，并记录日志。
        """
        logger.info("尝试数据库连接...")
        if self.connection is None or not self.connection.open:
            try:
                self.connection = pymysql.connect(host=self.host,
                                                  user=self.user,
                                                  password=self.password,
                                                  port=self.port,
                                                  database=self.db)
                logger.info("数据库连接成功。")
            except Exception as e:
                logger.error(f"连接数据库时出错：{e}")
                raise

    def execute_query(self, query):
        """
        执行SQL查询。

        参数:
        - query: 要执行的SQL查询语句。

        返回:
        - 查询结果的集合。
        """
        logger.debug(f"执行查询：{query}")
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                logger.info("查询执行成功。")
                return results
        except Exception as e:
            logger.error(f"执行查询时出错：{e}")
            raise

    def execute_update(self, query):
        """
        执行SQL更新操作。

        参数:
        - query: 要执行的SQL更新语句。

        返回:
        - 更新操作是否成功。
        """
        logger.debug(f"执行更新：{query}")

        try:
            with self.connection.cursor() as cursor:
                rows_affected = cursor.execute(query)
                self.connection.commit()
                logger.info("更新执行成功。")
                return rows_affected > 0
        except Exception as e:
            self.connection.rollback()
            logger.error(f"执行更新时出错：{e}")
            raise

    def execute_delete(self, query):
        """
        执行SQL删除操作。

        参数:
        - query: 要执行的SQL删除语句。

        返回:
        - 删除操作是否成功。
        """
        logger.debug(f"执行删除：{query}")

        try:
            with self.connection.cursor() as cursor:
                rows_deleted = cursor.execute(query)
                self.connection.commit()
                logger.info("删除操作成功。")
                return rows_deleted > 0
        except Exception as e:
            self.connection.rollback()
            logger.error(f"执行删除时出错：{e}")
            raise

    # 插入操作
    def execute_insert(self, query):
        """
        执行SQL插入操作。

        参数:
        - query: 要执行的SQL插入语句。

        返回:
        - 插入操作是否成功。
        """
        logger.debug(f"执行插入：{query}")
        self.connect()
        try:
            with self.connection.cursor() as cursor:
                rows_affected = cursor.execute(query)
                self.connection.commit()
                logger.info("插入操作成功。")
                return rows_affected > 0
        except Exception as e:
            self.connection.rollback()
            logger.error(f"执行插入时出错：{e}")
            raise

    def close(self):
        """
        关闭与数据库的连接。

        如果存在活动的连接，将其关闭，并记录日志。
        """
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已关闭。")


if __name__ == '__main__':
    db = DatabaseConnection()
    db.connect()
