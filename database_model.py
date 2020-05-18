from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_login import UserMixin
import os
from werkzeug.security import generate_password_hash,check_password_hash
db = SQLAlchemy()

class Caregiver(db.Model):
    __tablename__ = 'caregiver'
    cgid = db.Column(db.Integer,primary_key=True)
    label = db.Column(db.String(15))
    row_id = db.Column(db.Integer)
    description = db.Column(db.String(30))
    def __repr__(self):
        return "<cgid>:{0}".format(self.cgid)
    def __init__(self,**kwargs):
        for name,var in kwargs.items():
            self.__dict__[name] = var

class Patient(db.Model):
    __tablename__ = 'patients'
    row_id = db.Column(db.Integer)
    subject_id = db.Column(db.Integer,primary_key=True)
    gender = db.Column(db.String(5))
    dob = db.Column(db.DateTime)
    dod = db.Column(db.DateTime)
    dod_hosp = db.Column(db.DateTime)
    dod_ssn = db.Column(db.DateTime)
    expire_flag = db.Column(db.String(20))

    labs = db.relationship('LabEvent',backref='patient')
    #.cpts = db.relationship('Cpt',backref='cpts')
    events = db.relationship('DataTimeEvent',backref='patient')
    prescriptions = db.relationship('Prescription',backref='patient')




    def __repr__(self):
        return "ID:<%r>" % self.subject_id

class Admission(db.Model):
    __tablename__ = 'admissions'
    row_id = db.Column(db.Integer,primary_key=True)
    subject_id = db.Column(db.Integer)
    hadm_id = db.Column(db.Integer)
    admittime = db.Column(db.DateTime)
    dischtime = db.Column(db.DateTime)
    deathtime = db.Column(db.DateTime)
    admission_type = db.Column(db.String(50))
    admission_location = db.Column(db.String(50))
    discharge_location = db.Column(db.String(50))
    insurance = db.Column(db.String(255))
    language = db.Column(db.String(10))
    religion = db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    ethnichity = db.Column(db.String(50))
    edregtime = db.Column(db.DateTime)
    edouttime = db.Column(db.DateTime)
    diagnosis = db.Column(db.String(50))
    hospital_expire_flag = db.Column(db.SmallInteger)
    has_chartevents_data = db.Column(db.SmallInteger)

    def __repr__(self):
        return "admit_time:{0},subject_id:{1}".format(self.admittime,self.subject_id)

class Cpt(db.Model):
    __tablename__ = 'cpt'
    row_id = db.Column(db.Integer,primary_key=True)
    subject_id = db.Column(db.Integer)
    hadm_id = db.Column(db.Integer)
    costcenter = db.Column(db.String(10))
    chartdate = db.Column(db.DateTime)
    cpt_cd = db.Column(db.String(15))
    cpt_number = db.Column(db.Integer)
    cpt_suffix = db.Column(db.String(5))
    ticket_id_seq = db.Column(db.Integer)
    sectionheader = db.Column(db.String(50))
    subsectionheader = db.Column(db.String(300))
    description = db.Column(db.String(200))


class d_cpt(db.Model):
    __tablename__ = 'd_cpt'
    row_id = db.Column(db.Integer,primary_key=True)          
    category = db.Column(db.SmallInteger)           
    sectionrange = db.Column(db.String(100))
    sectionheader = db.Column(db.String(50))     
    subsectionrange = db.Column(db.String(100))     
    subsectionheade = db.Column(db.String(100))
    codesuffix = db.Column(db.String(300))            
    mincodeinsubsection = db.Column(db.Integer)
    maxcodeinsubsection = db.Column(db.Integer)

class d_labitems(db.Model):
    __tablename__ = 'd_labitems'
    row_id = db.Column(db.Integer)
    itemid = db.Column(db.Integer,primary_key=True)
    label = db.Column(db.String(100))
    fluid = db.Column(db.String(100))
    category = db.Column(db.String(100))
    loinc = db.Column(db.String(100))


class DataTimeEvent(db.Model):
    __tablename__ = "datatimeevent"
    row_id = db.Column(db.Integer,primary_key=True) 
    subject_id = db.Column(db.Integer,db.ForeignKey('patients.subject_id'))
    hadm_id = db.Column(db.Integer)   
    icustay_id = db.Column(db.Integer)  
    itemid = db.Column(db.Integer)     
    charttime = db.Column(db.DateTime)
    storetime = db.Column(db.DateTime)  
    cgid = db.Column(db.Integer)      
    value = db.Column(db.DateTime)     
    valueuom = db.Column(db.String(50))
    warning = db.Column(db.SmallInteger)  
    error = db.Column(db.SmallInteger)
    resultstatus = db.Column(db.String(50))
    stopped = db.Column(db.String(50))


class LabEvent(db.Model):
    __tablename__ = 'labevents'
    row_id = db.Column(db.Integer,primary_key=True) 
    subject_id = db.Column(db.Integer,db.ForeignKey('patients.subject_id'))
    hadm_id = db.Column(db.Integer)   
    itemid = db.Column(db.Integer)  
    charttime = db.Column(db.DateTime)
    value = db.Column(db.String(200))
    valuenum = db.Column(db.Numeric)
    valueuom = db.Column(db.String(20))
    flag = db.Column(db.String(20))


class Prescription(db.Model):
    __tablename__ = "prescription"
    row_id = db.Column(db.Integer,primary_key=True)
    subject_id = db.Column(db.Integer,db.ForeignKey('patients.subject_id'))
    hadm_id = db.Column(db.Integer)       
    icustay_id = db.Column(db.Integer)       
    startdate = db.Column(db.DateTime)
    enddate = db.Column(db.DateTime)      
    drug_type = db.Column(db.String(120))     
    drug  = db.Column(db.String(120))        
    drug_name_po = db.Column(db.String(120))
    drug_name_ge  = db.Column(db.String(120))
    formulary_drug  = db.Column(db.String(120))
    gsn = db.Column(db.String(120))
    ndc = db.Column(db.String(120))        
    prod_strength = db.Column(db.String(120)) 
    dose_val_rx = db.Column(db.String(120))   
    dose_until_rx  = db.Column(db.String(120)) 
    form_val_disp  = db.Column(db.String(120))
    form_unit_disp  = db.Column(db.String(120))
    route = db.Column(db.String(120))
    def __init__(self,**kwargs):
        for caption,val in kwargs.items():
            self.__dict__[caption] = val
            print(caption,val)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key= True,autoincrement=True)
    Email = db.Column(db.String(50))
    pwd  = db.Column(db.String(50))
    name = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
        raise AttributeError('password is not a readable attibute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return "<name>:{0}".format(self.name)
    # def __init__(self,id,Email,pwd,name):
    #     self.Email = Email
    #     self.pwd = pwd
    #     self.name = name


