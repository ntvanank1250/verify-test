from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas

# CUSTOMER


def get_server(db: Session, ip: int):
    return db.query(models.Server).filter(models.Server.ip == ip).first()

def get_servers(db:Session):
    return db.query(models.Server).all()

def get_domain(db: Session, domain: int):
    return db.query(models.Domain).filter(models.Domain.domain == domain).first()

def get_domains(db:Session):
    return db.query(models.Domain).all()

def get_list_servers(db:Session):
    servers = get_servers(db)
    list_ip = list()
    for server in servers:
        if server.ip:
            list_ip.append(str(server.ip))
    return list_ip

def get_list_domains(db:Session):
    domains = get_domains(db)
    list_domain = list()
    for domain in domains:
        if domain.domain:
            list_domain.append(str(domain.domain))
    return list_domain