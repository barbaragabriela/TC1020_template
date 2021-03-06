import pymysql
import sys

class Database:
    def __init__(self):
        # host = "127.0.0.1"
        host = "localhost"
        user = "root"
        password = "root"
        db = "StayHome"
        port = 8889

        self.con = pymysql.connect( host=host, 
                                    user=user, 
                                    password=password, 
                                    db=db, 
                                    port=port, 
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def list_members(self):
        query = '''
                SELECT * 
                FROM Member
                '''
        print('Query: {}'.format(query), file=sys.stdout)
        self.cur.execute(query)
        result = self.cur.fetchall()

        return result


    def list_member(self, member_no, member_name):
        query = '''
                SELECT *
                FROM Member
                '''
        if member_no != '':
            query += 'WHERE memberNo = {}'.format(member_no)
            if member_name != '':
                query += 'AND fName = \'{}\''.format(member_name)
        elif member_name != '':
            query += 'WHERE fName = \'{}\''.format(member_name)

        print('Query: {}'.format(query), file=sys.stdout)
        self.cur.execute(query)
        result = self.cur.fetchall()

        return result


    def insert_member(self, fName, lName, sex, dob, address):
        query = '''
                INSERT INTO Member (fName, lName, sex, DOB, address, dateJoined)
                VALUES ('{}', '{}', '{}', '{}', '{}', NOW())
                '''.format(fName, lName, sex, dob, address)
        print('Query: {}'.format(query), file=sys.stdout)
        self.cur.execute(query)
        self.con.commit()


    def delete_member(self, member_no):
        query = '''
                DELETE FROM Member
                WHERE memberNo = {}
                '''.format(member_no)
        print('Query: {}'.format(query), file=sys.stdout)
        self.cur.execute(query)
        self.con.commit()


    def SP_list_members(self):
        self.cur.callproc('GetAllMembers')
        result = self.cur.fetchall()

        return result


    def top_and_bottom_clients(self):
        query = '''
                select CONCAT(fName,' ',lName) Nombre,
                       'Con mas videos rentados' AS Posicion
                from Member
                where memberNo in
                (select memberNo
                from RentalAgreement
                group by memberNo
                having count(videoNo) >= all
                          (select count(videoNo)
                           from RentalAgreement
                           group by memberNo))
                UNION
                select CONCAT(fName,' ',lName)Nombre, 'Con menos videos rentados' AS Posicion
                from Member
                where memberNo in
                (select memberNo
                from RentalAgreement
                group by memberNo
                having count(videoNo) <= all
                          (select count(videoNo)
                           from RentalAgreement
                           group by memberNo))
                '''
        print('Query: {}'.format(query), file=sys.stdout)
        self.cur.execute(query)
        result = self.cur.fetchall()

        return result
