/*
Log for every request to (and response from) Antarika
oid								: surrogate primary key, may be same as requestId
status							: RequestReceived, SentForProcessing, ReceivedAfterProcessing, ResponseSent
requestReceivedOn				: timestamp when request was received from calling service
responseSentOn					: timestamp when response was sent to calling service
requestingProduct				: which prouct sent the request
requestingService				: which service sent the request
requestJson						: full Json payload of the request
responseJson					: full Json payload of the response
*/
create table 					AntarikaRequestLog
(
oid								varchar(128)							not null,
requestId						varchar(128)							not null,
status							varchar(32)								not null,
requestReceivedOn				timestamp								not null,
responseSentOn					timestamp,
requestingProduct				varchar(32)								not null,
requestingService				varchar(128)							not null,
requestJson						text									not null,
responseJson					text,
constraint						ck_Status_Antarika						check		(status = 'RequestReceived' or status = 'SentForProcessing' or status = 'ReceivedAfterProcessing' or status = 'ResponseSent'),
constraint						pk_AntarikaRequestLog					primary key	(oid)
);



/*
Audit Log for tracing every change in every table
oid 							: primary key
sectionName 					: name of the section under which the change was performed (Based on client readability)
tableName 						: name of the table for which the trace is
rowKey 							: oid of the row for which the trace is
timeOfAction 					: time of action
actionType 						: (I)nsert, (E)dit, (D)elete
actionSource 					: (U)ser, (S)ystem, (A)dmin
actionUser 						: Login username if from user end, or System if from system or A if by Admin
rowImageBefore 					: JSON representation of all rows (valid for update and delete), JSON must be line by line for diff capability
rowImageAfter 					: JSON representation of all rows (valid for insert and after), JSON must be line by line for diff capability
*/
create table 					AuditLog
(
oid 							varchar(128) 							not null,
sectionName 					varchar(200),
tableName 						varchar(64) 							not null,
rowKey 							varchar(64) 							not null,
timeOfAction 					timestamp 								not null,
actionType 						varchar(16) 							not null,
actionSource 					varchar(16) 							not null,
actionUser 						varchar(64) 							not null,
rowImageBefore 					text,
rowImageAfter 					text,
constraint 						c_actionType_AuditLog 					check 		(actionType = 'I' or actionType = 'E' or actionType = 'D'),
constraint 						c_actionSource_AuditLog 				check 		(actionSource = 'U' or actionSource = 'S' or actionSource = 'A'),
constraint 						p_AuditLog 								primary key (oid)
);

/*
This table to be used to store Request sent by client apps like androidApp.
requestId 						: Request Id sent to PlatForm
requestDetail 					: Request Packet
requestType 					:
requestDate 					:
requstStatus 					: Association status with system i. e. Received(R), Processed(P), FailedProcessed(FP)
traceId 						:
*/
create table 					ClientRequestLog
(
oid 							varchar(128),
requestId 						varchar(256) 							not null,
requestType 					varchar(200) 							not null,
requestDate 					timestamp 								not null,
requestDetail 					text 									not null,
requstStatus 					varchar(100) 							not null,
traceId 						varchar(64),
createdBy 						varchar(64) 							not null,
createdOn						timestamp 								not null,
updatedBy 						varchar(64),
updatedOn 						timestamp,
constraint 						p_ClientRequestLog 						primary key (oid)
);

/*
This table to be used to store Response sent to client apps like androidApp.
requestId 						: Response Id to be sent by csbPlatForm
responseDate 					: Response Packet
responseDetail 					: Association status with system i. e. submitted(S), closed(C)
responseStatus 					:
traceId 						:
*/
create table 					ClientResponseLog
(
oid 							varchar(200),
requestId 						varchar(256) 							not null,
responseDate 					timestamp 								not null,
responseDetail 					text 									not null,
responseStatus 					varchar(100) 							not null,
traceId 						varchar(64),
createdBy 						varchar(64) 							not null,
createdOn						timestamp 								not null,
updatedBy 						varchar(64),
updatedOn 						timestamp,
constraint 						p_ClientResponseLog 					primary key (oid)
);


/*
Logback related sequences and tables
*/
create sequence					logging_event_id_seq minvalue 1 start 1;

create table 					logging_event
(
timestmp 						bigint 									not null,
formatted_message 				text 									not null,
logger_name 					varchar(254) 							not null,
level_string 					varchar(254) 							not null,
thread_name 					varchar(254),
reference_flag 					smallint,
arg0 							varchar(254),
arg1 							varchar(254),
arg2 							varchar(254),
arg3 							varchar(254),
caller_filename 				varchar(254),
caller_class 					varchar(254) 							not null,
caller_method 					varchar(254) 							not null,
caller_line 					char(4) 								not null,
event_id 						bigint 									default 	nextval('logging_event_id_seq'),
constraint 						pk_logging_event 						primary key (event_id)
);

create table					logging_event_property
(
event_id 						bigint 									not null,
mapped_key 						varchar(254) 							not null,
mapped_value 					varchar(1024),
constraint 						fk_event_id_logging_event_property 		foreign key (event_id)
																		references 	logging_event(event_id),
constraint 						pk_logging_event_property 				primary key (event_id, mapped_key)
);

create table 					logging_event_exception
(
event_id 						bigint 									not null,
i 								smallint 								not null,
trace_line 						varchar(254) 							not null,
constraint 						fk_event_id_logging_event_exception 	foreign key (event_id)
																		references 	logging_event(event_id),
constraint 						pk_logging_event_exception 				primary key (event_id, i)
);