#install airflow via pip with constraints
AIRFLOW_VERSION=2.9.3
PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow[google]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

#set AIRFLOW_HOME based on current directory
export AIRFLOW_HOME=$(pwd)

#setup database based on AIRFLOW_HOME
airflow db migrate

#create user account to login to airflow
USERNAME=admin
FIRSTNAME=data
LASTNAME=engineer
PASSWORD=<ENTER YOUR PASSWORD>
EMAIL=<ENTER YOUR EMAIL>

airflow users create --username USERNAME --firstname FIRSTNAME --lastname LASTNAME --role Admin --password PASSWORD --email EMAIL

