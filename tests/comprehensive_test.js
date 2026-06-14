// Test 1: Callback functions & Array map/filter/reduce
let numbers = [1, 2, 3, 4, 5];
let doubled = numbers.map(x => x * 2);
let evens = numbers.filter(x => x % 2 === 0);
let sum = numbers.reduce((acc, curr) => acc + curr, 0);
console.log("Doubled: " + doubled.join(", "));
console.log("Evens: " + evens.join(", "));
console.log("Sum: " + sum);

// Test 2: Array find, some, every
let found = numbers.find(x => x > 3);
let hasSome = numbers.some(x => x > 4);
let hasAll = numbers.every(x => x > 0);
console.log("Found > 3: " + found);
console.log("Some > 4: " + hasSome);
console.log("Every > 0: " + hasAll);

// Test 3: String methods
let original = "  JavaScript Interpreter  ";
let trimmed = original.trim();
console.log("Trimmed: '" + trimmed + "'");
console.log("Upper: " + trimmed.toUpperCase());
console.log("Lower: " + trimmed.toLowerCase());
console.log("Slice: " + trimmed.slice(0, 4));
console.log("Substring: " + trimmed.substring(4, 10));
console.log("Includes Java: " + trimmed.includes("Java"));
console.log("Starts with Java: " + trimmed.startsWith("Java"));
console.log("Ends with Interpreter: " + trimmed.endsWith("Interpreter"));
console.log("IndexOf Script: " + trimmed.indexOf("Script"));
console.log("Replace: " + trimmed.replace("Script", "JS"));
console.log("ReplaceAll: " + "foo-bar-foo".replaceAll("foo", "baz"));

// Test 4: Math object
console.log("Math.PI check: " + (Math.PI > 3.14));
console.log("Math.abs: " + Math.abs(-5));
console.log("Math.ceil: " + Math.ceil(4.2));
console.log("Math.floor: " + Math.floor(4.7));
console.log("Math.round: " + Math.round(4.5));
console.log("Math.sqrt: " + Math.sqrt(16));
console.log("Math.pow: " + Math.pow(2, 3));
console.log("Math.max: " + Math.max(1, 5, 2));
console.log("Math.min: " + Math.min(1, 5, 2));

// Test 5: Date handling
// Create date for Jun 14 2024
let date = new Date("2024-06-14");
console.log("Year: " + date.getFullYear());
console.log("Month: " + date.getMonth()); // Jun is month 5 (0-indexed)
console.log("Date: " + date.getDate());

// Test 6: Spread/Rest in functions
function sumAll(...args) {
    return args.reduce((a, b) => a + b, 0);
}
console.log("Rest param sum: " + sumAll(1, 2, 3, 4));

// Test 7: Switch statement & Do-while
let x = "apple";
switch (x) {
    case "banana":
        console.log("It's a banana");
        break;
    case "apple":
        console.log("It's an apple");
        break;
    default:
        console.log("Unknown fruit");
}

let count = 0;
do {
    count++;
} while (count < 3);
console.log("Do-while count: " + count);
