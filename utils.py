
import re
import subprocess
import dns.resolver
from app import database

SessionLocal = database.SessionLocal

class DomainConfig:
    def __init__(self,name=None,domain_type = None,list_IP =list()):
        self.name = name
        self.domain_type = domain_type
        self.list_IP = list_IP
    def reset_domain(self):
        self.name = None
        self.domain_type = None
        self.list_IP = list()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Get db


def format_domain(domain):
    # Loại bỏ khoảng trắng ở đầu và cuối chuỗi
    domain = domain.strip()

    # Kiểm tra định dạng địa chỉ domain sử dụng regex
    pattern = r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$'
    match = re.match(pattern, domain)
    
    if match:
        # Chuẩn hóa thành lowercase
        domain = domain.lower()
        return domain
    else:
        # Địa chỉ domain không hợp lệ
        return None

def run_dig(domain):
    try:
        # Chạy câu lệnh dig và lấy kết quả đầu ra
        result = subprocess.check_output(['dig', domain]).decode('utf-8')
        print (result)
        return result
    except subprocess.CalledProcessError as e:
        # Xử lý lỗi nếu câu lệnh dig không thành công
        print(str(e))
        return str(e)

def get_ip(domain,domain_config=DomainConfig()):
    domain_config.reset_domain()
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8"]
    domain_config.domain_type = "CNAME"
    try:
        resolver_answers = resolver.query(domain, "CNAME")
    except:
        domain_config.domain_type = "A"
    if domain_config.domain_type == "A":
        try:
            resolver_answers = resolver.query(domain, "A")
        except dns.exception.DNSException as err:
            print(err)
    for answer in resolver_answers:
        domain_config.list_IP.append(str(answer))
    return domain_config

def check_string(string):
    pattern = r"\.vccloud\."
    match = re.search(pattern, string)
    if match:
        return True
    else:
        return False