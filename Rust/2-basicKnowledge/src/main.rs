fn main() {
    let sample_list: [i32; 5] = [10, 20, 30, 40, 50];

    // 列表遍历
    // 1
    for idx in 0..sample_list.len(){
        println!("line:{}, {}", idx+1, sample_list[idx]);
    }
    // 2
    for (idx, item) in sample_list.iter().enumerate(){
        println!("line:{}, {}", idx+1, item);
    }

    // stack and heap
    let mut string1 = String::from("hello");
    // let string2 = string1; 这儿会报error，此处string1的值将会move给string2
    // 所以string1 相当于离开了作用域，此时string1所在内存的值就被释放了
    // 只是将stack上的数据进行了拷贝(指针地址，容量等数据)

    // 这里使用clone()实现了类似深拷贝的功能，将string1在heap上的值做了一份拷贝
    // 在heap上新开辟了一段内存
    let string2 = string1.clone();
    println!("string1:{}, string2:{}", string1, string2);
    println!("edit string1 from 'hello' -> 'hello world'");
    string1.push_str(", world");
    println!("string1:{}, string2:{}", string1, string2);


    // 在直接将变量传入函数时也会发生move行为，这将导致变量的值发生了move，从而被移除作用域
    // 但是不可变类型的值就不会有这个问题
    let sample_int = 10;
    takes_ownership(string1);
    // println!("string1: {}", string1); // borrow of moved value: `string1`

    makes_copy(sample_int);
    println!("sample_int:{}", sample_int);

    // 如果使用引用进行传参，就可以解决这类问题
    // 引用传参传入的是地址，不会影响到heap上的值
    let string3 = String::from("hello");
    takes_ownership_ref(&string3);
    println!("string3 also can be visit: {}", string3);


}

fn takes_ownership(some_string: String) { // some_string 进入作用域
    println!("takes_ownership[some_string]: {}", some_string);
} // 这里，some_string 移出作用域并调用 `drop` 方法。占用的内存被释放

fn makes_copy(some_integer: i32) { // some_integer 进入作用域
    println!("makes_copy[some_integer]: {}", some_integer);
} // 这里，some_integer 移出作用域。不会有特殊操作

fn takes_ownership_ref(some_string: &String) { // some_string 进入作用域
    println!("some_string :{}, len:{}", some_string, some_string.len());
} // 这里，some_string 移出作用域并调用 `drop` 方法。占用的内存被释放
