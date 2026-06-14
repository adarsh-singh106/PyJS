# **THUNDER HACKATHON 2.0**

## **BUILD YOUR OWN JAVASCRIPT**

### **1. Hackathon Overview**

Your task is NOT to write JavaScript, but to BUILD something that can RUN JavaScript! You will write a program in any language (Python, Java, C++, ...) that accepts JavaScript code as input and executes it, producing the correct output.

**1.1 What You Need to Build**

**Your program must:**

- Accept a JavaScript code snippet as input (via file, stdin, or command-line argument)
- Execute that JavaScript code correctly
- Print the output to stdout, exactly matching the expected result
- Pass all 5 provided test cases

### **2. Rules & Constraints**

| **PROHIBITED** | JavaScript, TypeScript, CoffeeScript, or any JS-transpiled language as your primary submission language. |  |
| --- | --- | --- |
| ALLOWED | You can use any LLM tools |  |

**2.1 Allowed Languages (Examples)**

**The following are permitted  but any non-JS language is fine:**

| Python | Java | C / C++ | Rust / Go |
| --- | --- | --- | --- |
| Ruby | PHP | Kotlin / Swift | Haskell / Lua |

### **3. Test Cases**

**Your program will be evaluated against 5 test cases. Each is worth 20 points. Your solution must pass the test case's JavaScript code through your runtime and produce the exact expected output shown below.**

| **Test Case 1: Odd / Even Checker** |  |
| --- | --- |
| **JS Code** | let num = 7; 
if (num % 2 === 0) { 
    console.log(num + " is Even"); 
} else { 
    console.log(num + " is Odd"); 
} |
| **Expected Output** | 7 is Odd |

| **Test Case 2: Triangle Pattern using For Loop** |  |
| --- | --- |
| **JS Code** | for (let i = 1; i <= 5; i++) { 
    let row = ""; 
  
    for (let j = 1; j <= i; j++) { 
        row += "*"; 
    } 
  
    console.log(row); 
} |
| **Expected Output** | *****  
*** ***  
*** * ***  
*** * * ***  
*** * * * *** |

| **Test Case 3: Armstrong Number**  |  |
| --- | --- |
| **JS Code** | function isArmstrong(num) { let temp = num; let sum = 0; 
while (temp > 0) {
    let digit = temp % 10;
    sum += digit ** 3;
    temp = Math.floor(temp / 10);
}

return sum === num;
  
} 
console.log(isArmstrong(153));
console.log(isArmstrong(123)); |
| **Expected Output** 
 | true //153 
false // 123 |

| **Test Case 4: Array Reverse** |  |
| --- | --- |
| **JS Code** | let arr = [1, 2, 3, 4, 5]; 
let reversed = [...arr].reverse(); 
console.log("Original: " + arr.join(", ")); 
console.log("Reversed: " + reversed.join(", ")); |
| **Expected Output** | **Original: 1, 2, 3, 4, 5** 
**Reversed: 5, 4, 3, 2, 1** |

| **Test Case 5: String Palindrome Check** |  |
| --- | --- |
| **JS Code** | let str = "racecar"; 
let reversed = str.split("").reverse().join(""); 
if (str === reversed) { 
    console.log(str + " is a Palindrome"); 
} else { 
    console.log(str + " is not a Palindrome"); 
} |
| **Expected Output** | **racecar is a Palindrome** |

### **4. Scoring & Evaluation**

| **TC #** | **Test Case** | **Points** |
| --- | --- | --- |
| TC-1 | Odd/Even Checker | 20 |
| TC-2 | Triangle Pattern | 20 |
| TC-3 | Armstrong Number | 20 |
| TC-4 | Array Reverse | 20 |
| TC-5 | String Palindrome | 20 |
| **TOTAL SCORE** |  | **100** |

### **Hidden Test Cases ****

There will be additional hidden test cases used during final evaluation.

These hidden test cases will test similar JavaScript concepts with different inputs, edge cases, and slight variations.

Your runtime should be robust enough to handle any valid JavaScript code covered in class, not just the sample examples provided.

The implementation should support the following JavaScript features:

- Variable declarations (`let`, `const`)
- Primitive data types (`number`, `string`, `boolean`, `null`, `undefined`)
- Non-primitive/reference data types (`object`, `array`, `function`)
- Arithmetic, comparison, logical, and assignment operators
- Conditional statements (`if`, `else if`, `else`, `switch`)
- Loops (`for`, `while`, `do...while`)
- Arrays and common array operations such as `push()`, `pop()`, `shift()`, `unshift()`, `slice()`, `splice()`, `concat()`, `includes()`, `indexOf()`, `sort()`, and `reverse()`
- Strings and common string operations such as `replace()`, `replaceAll()`, `substring()`, `slice()`, `split()`, `trim()`, `toUpperCase()`, `toLowerCase()`, `includes()`, `startsWith()`, `endsWith()`, and `indexOf()`
- Objects and object manipulation
- Functions (function declarations, function expressions, and arrow functions)
- Callback functions
- Array methods such as `map()`, `filter()`, `reduce()`, `find()`, `some()`, and `every()`
- Math operations and the `Math` object, including random number generation (`Math.random()`)
- Date handling using the `Date` object
- Type conversion and coercion
- Spread and rest operators

**4.1 Tie-Breaking Criteria**

**If two submissions pass the same number of test cases, the winner is determined in this order:**

- Code quality, clarity, and structure (clean, readable code wins)
- Innovation of approach
- Performance: execution speed of test cases
- Earlier submission timestamp

### **5. Deadline:**

### **Sunday (14th June) 11:59 pm**

### 6. 🏆 **Prize Pool**

🥇 **Top 3 Winners** will receive a **1-Month Claude AI Pro Subscription**.

🎖️ **Ranks 4–10** will receive **₹500 each** as a cash prize.

Compete, innovate, and showcase your skills for a chance to win exciting rewards!

### 7. Submission :

Please ensure that all submissions meet the following requirements:

- The complete source code must be hosted on a **public GitHub repository**.
- Submit the **GitHub Repository Link** containing your solution.

> You repo must have a readme.md file that will have information about how to run your code
> 
- Share a post about your submission on **X (formerly Twitter)** and provide the **X Post Link**.

**Submission Link**