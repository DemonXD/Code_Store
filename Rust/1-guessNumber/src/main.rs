use rand::{Rng, thread_rng};

fn main(){
    let mut count = 0;
    // generate a random int
    let secret_num: u32 = thread_rng().gen_range(0..101);
    println!("The secret number: {}!", secret_num);

    println!("Guess the number!");
    println!("Please input a number:");
    
    
    loop {
        let mut guess = String::new();

        std::io::stdin().read_line(&mut guess)
            .expect("Failed to read line");
    
        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };
    
        match guess.cmp(&secret_num) {
            std::cmp::Ordering::Less => {
                count += 1;
                println!("Too small");
            },
            std::cmp::Ordering::Greater => {
                count += 1;
                println!("Too big");
            },
            std::cmp::Ordering::Equal => {
                println!("Congrat!");
                break;
            },
        }
        if count >= 3{
            println!("over try times!");
            break;
        }
    }

}
