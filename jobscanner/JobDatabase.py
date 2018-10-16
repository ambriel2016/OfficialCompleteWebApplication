import random
import sqlite3
import Nlp
import datetime
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


class JobDatabase:
    global title, c1, c2, c3, c4, c5, dbfile
    title = "keywords"
    c1 = "user"
    c2 = "job_id"
    c3 = "keyword"
    c4 = "count"
    c5 = "dt"
    dbfile = "final_words.db"

    @staticmethod
    def process_data(user_dict={}):
        lm = WordNetLemmatizer()

        db = sqlite3.connect("final_words.db")
        cur = db.cursor()
        db.execute("CREATE TABLE IF NOT EXISTS inputs (user TEXT, job_number TEXT, job TEXT, dt TEXT)")
        db.execute(
            "CREATE TABLE IF NOT EXISTS keywords (" + c1 + " TEXT, " + c2 + " TEXT, " + c3 + " TEXT, " + c4 + " INTEGER, " + c5 + " TEXT)")
        db.execute(
            "CREATE TABLE IF NOT EXISTS lemmas ( user TEXT, " + c2 + " TEXT, lemma TEXT, count INTEGER, " + c5 + " TEXT)")

        for user_name, jobs in user_dict.items():
            jd_list = []
            for job in jobs:
                job = Nlp.Nlp.central(job)
                jd_list.append(job)

            for description in jd_list:
                job_num = random.randint(10000, 100000)

                try:
                    # this checks to see if the user has already entered an identical job
                    # description, if he hasn't it will input it
                    cur.execute("SELECT * FROM inputs WHERE user = '" + user_name + "' AND job = '" + description + "'")
                    if cur.fetchall().__len__() == 0:
                        dtuser = datetime.datetime.now()
                        db.execute("INSERT INTO inputs (user, job_number, job, dt) VALUES('" + user_name + "', '" + str(
                            job_num) + "', '" + description + "', '" + str(dtuser) + "')")

                        ###transfer from inputs table to main table
                        cur.execute("SELECT * FROM inputs WHERE job_number = '" + str(job_num) + "'")
                        for user_name2, job_num2, desc2, dtuser2 in cur.fetchall():
                            # clean up
                            desc2 = Nlp.Nlp.central(desc2)

                            # put in ordered dictionary
                            words_dict = Nlp.Nlp.return_dictionary(desc2)

                            for word, wcount in words_dict.items():
                                db.execute(
                                    "INSERT INTO keywords (user, job_id, keyword, count, dt) VALUES('" + user_name2 + "', '" + str(
                                        job_num2) + "', '" + word + "', " + str(wcount) + ", '" + str(dtuser2) + "')")

                            lemma_dict = Nlp.Nlp.return_lemma_dictionary(desc2)
                            for lword, lwcount in lemma_dict.items():
                                db.execute(
                                    "INSERT INTO lemmas (user, job_id, lemma, count, dt) VALUES('" + user_name2 + "', '" + str(
                                        job_num2) + "', '" + lword + "', " + str(lwcount) + ", '" + str(dtuser) + "')")
                except sqlite3.Error as er:
                    print(er)

        cur.close()
        db.commit()
        db.close()

    @staticmethod
    def sql_query(user_name):
        select = str("SELECT keyword, SUM(count), COUNT(keyword) AS count FROM keywords ")
        where = str("WHERE user = '" + user_name + "' AND count>0 ")
        group = "GROUP BY keyword "
        order = "ORDER BY COUNT(keyword) DESC, SUM(count) DESC, keyword"
        sql_query = str(select + where + group + order)
        return sql_query

    @staticmethod
    def lemma_sql_query(user_name):
        select = str("SELECT lemma, SUM(count), COUNT(lemma) AS count FROM lemmas ")
        where = str("WHERE user = '" + user_name + "' AND count>0 ")
        group = "GROUP BY lemma "
        order = "ORDER BY COUNT(lemma) DESC, SUM(count) DESC, lemma"
        lemma_sql_query = str(select + where + group + order)
        return lemma_sql_query
