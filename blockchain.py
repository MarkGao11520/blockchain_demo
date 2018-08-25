"""
create by gaowenfeng on 2018/8/25
"""
from app import create_app

__author__ = "gaowenfeng"

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



