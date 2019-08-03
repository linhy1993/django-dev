import pymysql


class Database():
    def __init__(self, truncate=False):
        self.db = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='movie')
        self.cursor = self.db.cursor()
        if truncate:
            self.truncate_table()

    def close_db(self):
        self.db.close()

    def _execute(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print(sql)
            self.db.rollback()

    def insert_movie(self, name, stars, release_time, score):
        sql = "INSERT INTO movies(name, stars, release_time, score) " \
              "VALUES ('%s', '%s', '%s', '%s')" % (name, stars, release_time, score)
        self._execute(sql=sql)

    def truncate_table(self):
        sql = "TRUNCATE table movies;"
        self._execute(sql=sql)

    def search_by_name(self, name):
        """Search by name"""
        sql = "SELECT * FROM movies WHERE name = '%s';" % (name)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def search_by_rank_range(self, rank=0, first=0, last=0):
        """Search by rank range"""
        if rank:
            sql = "SELECT * FROM movies WHERE id = %s;" % rank
        else:
            sql = "SELECT * FROM movies WHERE id BETWEEN %s AND %s;" % (first, last)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def search_by_score_range(self, below=0.0, above=0.0):
        """Search by score range"""
        sql = "SELECT * FROM movies WHERE score BETWEEN %s AND %s;" % (below, above)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def search_by_year(self, year=None, start=None, end=None):
        """Search by year or year range"""
        if start and end:
            sql = "SELECT * FROM movies WHERE YEAR(release_time) BETWEEN %s AND %s;" % (start, end)
        else:
            sql = "SELECT * FROM movies WHERE YEAR(release_time) = %s;" % year
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results


def test():
    db = Database()
    print(f"""
    search by name                      {db.search_by_name('霸王别姬')}
    search by rank 1                    {db.search_by_rank_range(rank=1)}
    search by rank 1 to 2               {db.search_by_rank_range(first=1, last=2)}
    search by score range 9.6 to 9.7    {db.search_by_score_range(below=9.6, above=9.7)}
    search by year from 1952 to 1953    {db.search_by_year(start=1952, end=1953)}
    search by specific year 1953        {db.search_by_year(year=1953)}
    """)


if __name__ == '__main__':
    test()
