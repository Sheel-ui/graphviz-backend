from openai import OpenAI
import pandasql as ps
import re
import os

class Generate:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def generateNull(self,df):
        result_df = ps.sqldf("Select * from df", locals())
        columns = result_df.columns.tolist()
        rows = result_df.values.tolist()
        result_type = "table"
        return {
            "result_type": result_type,
            "data": {
                "columns": columns,
                "rows": self.transform_data(rows,columns)
            }
        }

    def generate(self,text,df,filename):
        column_info = df.dtypes
        line1 = "I have a csv file with columns:\n"
        line2 = str(column_info)
        line3 = "My table name is df\n"
        line4 = "Write an SQL query:\n"
        prompt = line1+line2+line3+line4+text

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        query = response.choices[0].message.content

        if query.find("```sql")!=-1:
            start=query.find("```sql")
            end=query.rfind("```")
            query = query[start+6:end]
        
        result_df = ps.sqldf(query, locals())
        columns = result_df.columns.tolist()
        rows = result_df.values.tolist()
        result_type = "table"
        pattern = r'\bGROUP\s+BY\b'
        match = re.search(pattern, query, re.IGNORECASE)
        if match and len(columns)==2:
            data = []
            labels = []
            for row in rows:
                data.append(row[1])
                labels.append(row[0])

            return {
                "result_type": "graph",
                "data": {
                    "data": data,
                    "labels": labels,
                    "label": filename
                }
            }

        return {
            "result_type": result_type,
            "data": {
                "columns": columns,
                "rows": self.transform_data(rows,columns)
            }
        }
    
    def transform_data(self,rows,columns):
        transformed_data = []
        
        for row in rows:
            transformed_row = {}
            for i, column in enumerate(columns):
                transformed_row[column] = row[i]
            transformed_data.append(transformed_row)
        
        return transformed_data