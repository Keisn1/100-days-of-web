function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const secretNumber = getRandomInt(1, 15);

const maxAttempts = 5;
console.log('Guess the secret number: ');
let count = 0;
while(true){
    let guess = prompt("Please type in a number");
    guess = parseInt(guess);
    if(guess === null || guess == "q") {
        die("Ok, exiting");
    }
    if (isNaN(guess)){
        console.log("A number please");
        continue;
    }
    if (guess < secretNumber) {
        console.log("$(guess) is smaller than secretNumber");
    } else if (guess > secretNumber) {
        console.log("$(guess) is bigger than secretNumber");
    } else {
        console.log("You guessed it!");
    }

    count++;
    if(count == maxAttempts){die("You guessed enough times, the right answer was $(secretNumber)");}
}
