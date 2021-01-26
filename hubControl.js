////////////////////////////////////////////
//            GLOBAL VARIABLES
////////////////////////////////////////////
const os = require('os');
const hubInput = require('/scripts/modules/hubInput.js');
var _hub={};
//var primaryController={}, popupController={};

//##########################################
const onCommand = function(zone, command) {
//##########################################
console.log(`Enter onCommand for command: ${command}`);
var hubOutput = require('/scripts/modules/hubOutput.js');
var controller, task;

	if(_hub[zone].popupModule) {
		//module = _hub[zone].popupModule;
		_hub[zone].popupController = require(_hub[zone].popupModule);
		_hub[zone].popupModule = null;
		controller = _hub[zone].popupController;
	} else {
		_hub[zone].primaryController = require(_hub[zone].primaryModule);
		controller = _hub[zone].primaryController;
	};
	
	if(!controller.tasks[command]) return console.log(`Abort: Invalid command: ${command}`);
	
	task = `{"action": "runSequence", "sequence": ${JSON.stringify(controller.tasks[command])}}`;
	console.log(`For command: ${command}, Send task: ${task}`);
	hubOutput.sendControlTask(task);
};

//##########################################
const onFunction = function(zone, command) {
//##########################################
console.log(`Enter onFunction with ${command} in zone: ${zone}`);

	_hub[zone].isFunctionSet = null;
};
 
//##########################################
const onModuleSelected = function(zone, command) {
//##########################################
console.log(`Enter onModuleSelected with ${command} in zone: ${zone}`);

	_hub[zone].isModuleSelected = null;
	if(command == 'On/Off' || command == 'Set') command = 'Open';
	console.log(`Send command: ${command}`);
	return onCommand(zone, command);
};

//##########################################
const onSelectModule = function(zone, command) {
//##########################################
console.log(`Enter onSelectModule with ${command} in zone ${zone}`);

	_hub[zone].isFocusSet = null;
	
	if(_hub[zone].topics[command] && _hub[zone].topics[command].controller[command]) {
		_hub[zone].primaryModule = _hub[zone].topics[command].controller[command];
		_hub[zone].isModuleSelected = true;
		return console.log(`primaryModule selected : ${_hub[zone].primaryModule}`);
	};
	
	if(_hub[zone].topics[_hub[zone].focus] && _hub[zone].topics[_hub[zone].focus].controller[command]) {
		_hub[zone].popupModule = _hub[zone].topics[_hub[zone].focus].controller[command];
		//_hub[zone].isModuleSelected = true;
		return console.log(`popupModule selected: ${_hub[zone].popupModule}`);
	};
 };
 
//##########################################
const onInput = function(hubInput) {
try {
//##########################################
console.log(`Enter onInput, command: ${hubInput.command}, zone: ${hubInput.zone}`);
_hub[hubInput.zone] = require(`/scripts/modules/hubs/hub.zone.${hubInput.zone}.js`);
	
	if(_hub[hubInput.zone].isFocusSet) return onSelectModule(hubInput.zone, hubInput.command);
	if(_hub[hubInput.zone].isModuleSelected) return onModuleSelected(hubInput.zone, hubInput.command);
	//if(_hub[hubInput.zone].isFunctionSet) return onFunction(hubInput.zone, hubInput.command);

	if(hubInput.command == 'Focus') {_hub[hubInput.zone].isFocusSet = true; return console.log(`Set Focus Flag`);}

	if(hubInput.command == 'Set') hubInput.command = 'On/Off';

	if(hubInput.command == 'Silence/Sound') {
		if(_hub[hubInput.zone].isSilent)
			{hubInput.command = 'Sound';_hub[hubInput.zone].isSilent=false;}
		else
			{hubInput.command = 'Silence';_hub[hubInput.zone].isSilent=true;}
	};
	
	onCommand(hubInput.zone, hubInput.command);
}
catch(error) {
	console.log(`Unexpected Problem: ${error}`);
	console.error(error);
}};
		
////////////////////////////////////////////
//                MAIN
//Open server to listen for control input
////////////////////////////////////////////
console.log(`Started hubControl on ${os.hostname}`);

	hubInput.listen(onInput);
