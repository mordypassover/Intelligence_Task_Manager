# Intelligence_Task_Manager

## explanation:

this project handles agents and missions using a mysql database 
with 2 tables, missions and agents. the tables are created and contacted 
with DBConnection class and used by AgentDB and MissionDB to get add and 
alter data.
the classes are called by routs witch are used by users to create missions and agents,
get agent and mission stats and handel assignment 

## file build:

intelligence-task-manager
├── database
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore


## docker command:
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=**** \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

## agents table:
id	                INT,       AUTO_INCREMENT, PK,	primary key
name	            VARCHAR	,  agent name
specialty	        VARCHAR,   agent specialty
is_active	        BOOLEAN,   default: TRUE,  
completed_missions	INT,	   default: 0
failed_missions	    INT,	   default: 0
agent_rank	        VARCHAR,   ENUM(Junior / Senior / Commander )

## missions table:
id               	INT      AUTO_INCREMENT, PK	primary key
title             	VARCHAR	 title 
description	        TEXT	 mission description
location          	VARCHAR  mission location
difficulty	        INT	     1–10  
importance	        INT	     1–10 
status	            VARCHAR  default : NEW  ENUM(NEW, ASSIGNED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED)
risk_level	        VARCHAR  ato calc by difficulty *2 +importance
assigned_agent_id	INT|NULL agent id or null if not assigned


## DBConnection:

get_connection(), connects to DB
create_database(), creates database if not exists
create_tables(), creates tables if not exists


## AgentDB class:

create_agent(data)        creates new agent and returns created agent
get_all_agents()          lists all agents
get_agent_by_id(id)       gets agent by id else None
update_agent(id, data)    updates agent (excluding id which cont be updated)
deactivate_agent(id)      deactivates agent
increment_completed(id)	  adds 1 to completed_missions
increment_failed(id)	  adds 1 to failed_missions
get_agent_performance(id) gets performances, completed, failed, total and success_rate(persent)
count_active_agents()	  returns num of active agents

## MissionDB class:

create_mission(data)	          creates new mission and returns created mission
get_all_missions()	              lists all mission
get_mission_by_id(id)	          gets mission by id else None
assign_mission(m_id, a_id)	      assign mission to agent 
update_mission_status(id, status) changes status of mission
get_open_missions_by_agent(id)    lists all missions with status ASSIGNED or IN_PROGRESS 
count_all_missions()	          sums all missions returns sum
count_by_status(status)	          sums all missions by status returns sum
count_open_missions()	          sums all opened missions returns sum
count_critical_missions()         sums all critical missions returns sum
get_top_agent()                   gets agent with most completed_missions

## roles

1	rank must be Junior / Senior / Commander — else raises error.
2	difficulty and -importance must be between 1 -10 — else raises error.
3	risk_level is automatically calculated, user dose not enter it when creating mission.
4   agent with is_active=False cent be assign to mission.
5	agent cant have more then 3 missions opened (ASSIGNED / IN_PROGRESS) at same time.
6	if risk_level=CRITICAL — only Commander agents can be assigned to mission.
7	mission can be assigned only if NEW. after assignment: status=ASSIGNED.
8	only ASSIGNED missions can be started. then : status=IN_PROGRESS.
9	only IN_PROGRESS missions can be failed or completed
10	only NEW or ASSIGNED can be canceled, otherwise raise error.


## explain to run project:
clone github repo
go to project on bash, run:
    pip install requirements.txt
    docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD={your password}  \
    -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
