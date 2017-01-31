import os

class DevelopmentConfig(object):
	SQLALCHEMY_DATABASE_URI = "    postgres://qgtmtzhohhhnoh:f1c07c2b6b6fe956086d61572dc5659d3ed1ff6cdccd6913a771edf5a436b991@ec2-23-23-225-116.compute-1.amazonaws.com:5432/d92okdk8muv3nh"
	DEBUG = False
	SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", os.urandom(12))

class TestingConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/blogful-test"
	DEBUG = False
	SECRET_KEY = "Not secret"

class TravisConfig(object):
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
	DEBUG = False
	SECRET_KEY = "Not secret"
