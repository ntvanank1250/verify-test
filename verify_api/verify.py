from fastapi import Request, APIRouter, Form, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
import time
from utils import *
from app import crud, database, models, schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Home page


@router.get("/")
def get_verify(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/")
async def post_verify(request: Request, domain: str = Form(...), db: Session = Depends(get_db)):
    if format_domain(domain=domain):
        run_dig(domain)
        list_ip = get_ip(domain=domain).list_IP
        return templates.TemplateResponse("index.html", {"list_ip": list_ip, "domain": domain, "request": request})
    message = "Địa chỉ domain không hợp lệ"
    return templates.TemplateResponse("index.html", {"message": message, "request": request})

# Auto check


@router.get("/list-check")
def get_list_check(request: Request, db: Session = Depends(get_db)):
    domains = crud.get_list_domains(db=db)
    ips = crud.get_list_servers(db=db)
    params = list()
    for domain in domains:
        list_ip = list()
        list_domain_ip = list()
        if format_domain(domain=domain):
            domain_config = get_ip(domain=domain)
            list_domain_ip = domain_config.list_IP
            if domain_config.domain_type == "CNAME":
                for ip in list_domain_ip:
                    if check_string(ip):
                        list_ip.append(ip)
                if list_ip:
                    message = "Đã trỏ về IP trong danh sách"
                else:
                    message = "Không trỏ về IP trong danh sách"
            elif domain_config.domain_type == "A":
                for ip in list_domain_ip:
                    if ip:
                        if ip in ips:
                            list_ip.append(ip)
                if list_ip == [None] or not list_ip:
                    message = "Không trỏ về IP trong danh sách"
                elif len(list_ip) < len(list_domain_ip):
                    message = "Đã trỏ về IP trong danh sách và IP ngoài danh sách"
                else:
                    message = "Đã trỏ về IP trong danh sách"
            else:
                message = "Không dig được domain"
        else:
            message = "Địa chỉ domain không hợp lệ"
        param = {
            "domain": domain,
            "IP": list_domain_ip,
            "myIP": list_ip,
            "message": message
        }
        params.append(param)
    current_time = datetime.now()
    current_time = str(current_time).split(".")[0]
    print(current_time)
    print("#############################################################################################################")
    return templates.TemplateResponse("check.html", {"params": params, "current_time": current_time, "request": request})
