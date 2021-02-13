////////////////////////////////////////////
//            GLOBAL VARIABLES
////////////////////////////////////////////
const debug = require('/inputHub/core/debugLog.js').debug;
const webSocket = require('/root/node_modules/ws');

var connection = null, isConnected = null, activeSessions = {}, sessionId = 1;

//##########################################
onOpen =  function() {
//##########################################
console.log('Enter onOpen');
  //ws.send(Date.now());
};

//##########################################
onClose =  function() {
//##########################################
console.log('Enter onClose');

	openConnection();
};

//##########################################
onMessage = function(message) {
//##########################################
var payload = JSON.parse(message);

	debug.log(`Enter onMessage, Received server message: `, message);

	if(payload.type == 'auth_required') return connection.send('{"type": "auth", "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI1YmM0ZGYxNGY4ZGE0MTdkYTNhZjdkNjkwYzg0NDQ2ZSIsImlhdCI6MTYxMzAxMDQ4MiwiZXhwIjoxOTI4MzcwNDgyfQ.MffxNYX4VssITLgdZBPilKTq3p4R9RuoQP2yeeoyyPw"}');
	if(payload.type == 'auth_ok') return isConnected = true;
	if(payload.type != 'result') return console.log(`Unknown Message from wsOutput: `, message);

	console.log(` \n`);
	console.log(`==================================================================================================`);

	if(activeSessions[payload.id] && !payload.success) {
	//Report Session Error
		console.log(`Send error reply, sessionId: ${payload.id}, result: `, payload.result, `\ntask: `, activeSessions[payload.id].task);
		activeSessions[payload.id].onReply("***TASK FAILED***\n", message);
	};		

	delete activeSessions[payload.id]; //Delete completed session
	console.log(`Server result: messageId: ${payload.id}, status: ${payload.success}, result: `, payload.result);
};

//##########################################
runTask = function(input, reply) {
//##########################################
console.log(`Enter runTask`);
var task = JSON.parse(input);
var service, key, command, payload={};

	if(!isConnected) return console.log(`Abort runTask: Not connected to server`);
	if(task.length == 0) return console.log(`runTask Completed`);

	service = task[0];
	task.shift();
	key = Object.keys(service)[0];
	command = key.split('/');

	if(command.length == 1) {
		var duration = 0;
		if(command[0] == 'sleep') duration = service[key] * 1000;

		console.log(`Sleep: ${duration} millisecs`);
		setTimeout(function timeout() {
			runTask(JSON.stringify(task), reply);
		}, duration);
		
		return;
	};

	payload = {
		"id": sessionId, 
		"type": "call_service",	
		"domain": command[0],
		"service": command[1],
		"service_data": service[key]
	};
	
	activeSessions[sessionId] = {
		"task": payload,
		"onReply": reply
	};
	
	++sessionId;
		
	console.log(`Call service, id: ${payload.id}, domain: ${payload.domain}, service: ${payload.service}`);
	connection.send(JSON.stringify(payload));
	return runTask(JSON.stringify(task), reply);
};

//##########################################
openConnection = function() {
//##########################################
console.log(`Enter openConnection`);

	isConnected = false;
	if(connection) connection.close();
	
	connection = new webSocket('ws://192.168.0.160:8123/api/websocket', {});
	connection.on('open', onOpen);
	connection.on('close', onClose);
	connection.on('message', onMessage);
};

////////////////////////////////////////////
//                MAIN
//Open connection with Hub and send request
////////////////////////////////////////////
console.log('Loaded wsOutput.js');

	global.onOutput = runTask;
	//exports.runTask = runTask;
	openConnection();	