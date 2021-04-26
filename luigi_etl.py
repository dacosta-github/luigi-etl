from sqlalchemy import create_engine
import luigi
import pandas as pd
import sys
sys.path.insert(0, '../luigi-etl')

class QueryDB1(luigi.Task):
    def requires(self):
        return []
    
    def output(self):
        return luigi.LocalTarget("DB1_output.csv")
    
    def run(self):
        engine = create_engine('sqlite:///db1')
        results = pd.read_sql_query('SELECT * from names',engine)

        f = self.output().open('w')
        results.to_csv(f,encoding = 'utf-8',index=False,header=True,quoting=2)
        f.close()

class QueryDB2(luigi.Task):
    def requires(self):
        return []
    
    def output(self):
        return luigi.LocalTarget("DB2_output.csv")
    
    def run(self):
        engine = create_engine('sqlite:///db2')
        results = pd.read_sql_query('SELECT * from salaries',engine)

        f = self.output().open('w')
        results.to_csv(f,encoding = 'utf-8',index=False,header=True,quoting=2)
        f.close()


class CreateReport(luigi.Task):
    def requires(self):
        return [QueryDB1(),QueryDB2()]
    
    def output(self):
        return luigi.LocalTarget("./Report.csv")
    
    def run(self):
        df1 = pd.read_csv("DB1_output.csv", header = 0, encoding = 'utf-8',index_col = False)
        df2 = pd.read_csv("DB2_output.csv", header = 0, encoding = 'utf-8',index_col = False)
        df3 = pd.merge(df1,df2,how='inner',on=['id'])

        f = self.output().open('w')
        
        df1.to_csv(f,encoding = 'utf-8',index=False,header=True,quoting=2)
        
        f.close()


if __name__ == '__main__':
    luigi.run(main_task_cls=CreateReport,
              local_scheduler=False
            )