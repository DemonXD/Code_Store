pub fn math(op: fn(i32, i32) -> i32, a: i32, b: i32) -> i32 {
    return op(a, b);
}

fn sum(a: i32, b: i32) -> i32 {
    return a + b;
}