// Ex - 1: Function hoisting
sayHi();

function sayHi() {
    console.log("Hello");
}

// Ex - 2: Number, String, and Boolean constructors called as helper functions
console.log(Number("42"));
console.log(String(42));
console.log(Boolean(0));
