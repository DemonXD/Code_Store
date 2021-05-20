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
}
