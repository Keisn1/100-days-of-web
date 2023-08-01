function hello(name) {
    return 'Hello ' + name;
}

console.log(hello('bob'));
// print via console or alert
console.log('Hello World');
var name = 'bob';
// let is block scoped
let name1 = 'bob';
const minAge = 3;

// primitives
// arrays
names = ['bob', 'alice', 'julian'];
names.length
// inplace operations
names.sort();
names.reverse();
names.slice(1, 3);
names.push('Sarah');
names.pop()
names.shift()

for(let i=0; i<names.length; i++) {
    console.log(names[i])
}

my_age = 18
min_age = 12
if(my_age >= minAge) {
    console.log("I can drive")
} else {
    console.log("Nope, not allowed")
}
(my_age >= minAge) ? console.log('can drive') : console.log('not allowed')
names = ['bob', 'julian', 'mike', 'berta', 'quinton', 'tim', 'oliver']
for(let name of names) {
    if(name.startsWith('b')) {
        console.log(name)
    } else if (name.startsWith('q')){
        console.log(name + ' starts with q')
        break;
    }
}

function hello(name) {
    if(name === undefined) name = 'stranger';
    console.log('Hello ' + name);
}
function hello_1(name='stranger') {
    console.log(`Hello ${name}`);
}

let hello_2 = (name='stranger') => console.log(`Hello ${name}`)
hello()
hello_1()
hello_2()

