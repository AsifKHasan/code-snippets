var iWords = ['zero', ' one', ' two', ' three', ' four', ' five', ' six', ' seven', ' eight', ' nine'];
var ePlace = ['ten', ' eleven', ' twelve', ' thirteen', ' fourteen', ' fifteen', ' sixteen', ' seventeen', ' eighteen', ' nineteen'];
var tensPlace = ['', ' ten', ' twenty', ' thirty', ' forty', ' fifty', ' sixty', ' seventy', ' eighty', ' ninety'];
var inWords = [];

function convertAmount(numericValue) {
	numericValue = parseFloat(numericValue).toFixed(2);

	var amount = numericValue.toString().split('.');
	var taka = amount[0];
	var paisa = amount[1];
	return convert(taka) +" taka and "+ convert(paisa) + " paisa only";
}

var numReversed, inWords, actnumber, i, j;

function tensComplication() {
	if (actnumber[i] == 0) {
		inWords[j] = '';
	} else if (actnumber[i] == 1) {
		inWords[j] = ePlace[actnumber[i - 1]];
	} else {
		inWords[j] = tensPlace[actnumber[i]];
	}
}

function convert(numericValue) {
	inWords = []
	if(numericValue == "00" || numericValue =="0"){
		return 'zero';
	}
	var obStr = numericValue.toString();
	numReversed = obStr.split('');
	actnumber = numReversed.reverse();


	if (Number(numericValue) == 0) {
		return 'zero';
	}

	var iWordsLength = numReversed.length;
	var finalWord = '';
	j = 0;
	for (i = 0; i < iWordsLength; i++) {
		switch (i) {
			case 0:
				if (actnumber[i] == '0' || actnumber[i + 1] == '1') {
					inWords[j] = '';
				} else {
					inWords[j] = iWords[actnumber[i]];
				}
				inWords[j] = inWords[j] + '';
				break;
			case 1:
				tensComplication();
				break;
			case 2:
				if (actnumber[i] == '0') {
					inWords[j] = '';
				} else if (actnumber[i - 1] !== '0' && actnumber[i - 2] !== '0') {
					inWords[j] = iWords[actnumber[i]] + ' hundred';
				} else {
					inWords[j] = iWords[actnumber[i]] + ' hundred';
				}
				break;
			case 3:
				if (actnumber[i] == '0' || actnumber[i + 1] == '1') {
					inWords[j] = '';
				} else {
					inWords[j] = iWords[actnumber[i]];
				}
				if (actnumber[i + 1] !== '0' || actnumber[i] > '0') {
					inWords[j] = inWords[j] + ' thousand';
				}
				break;
			case 4:
				tensComplication();
				break;
			case 5:
				if (actnumber[i] == '0' || actnumber[i + 1] == '1') {
					inWords[j] = '';
				} else {
					inWords[j] = iWords[actnumber[i]];
				}
				if (actnumber[i + 1] !== '0' || actnumber[i] > '0') {
					inWords[j] = inWords[j] + ' lakh';
				}
				break;
			case 6:
				tensComplication();
				break;
			case 7:
				if (actnumber[i] == '0' || actnumber[i + 1] == '1') {
					inWords[j] = '';
				} else {
					inWords[j] = iWords[actnumber[i]];
				}
				inWords[j] = inWords[j] + ' crore';
				break;
			case 8:
				tensComplication();
				break;
			default:
				break;
		}
		j++;
	}


	inWords.reverse();
	for (i = 0; i < inWords.length; i++) {
		finalWord += inWords[i];
	}

	return finalWord.trim();
}
