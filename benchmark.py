import timeit
from auditor import score_password

PASSWORDS = [
    # Weak
    "abc",
    "password",
    "123456",
    "letmein",
    "qwerty",
    # Moderate
    "Password1",
    "Summer2024",
    "MyDog12345",
    "Welcome99",
    "Admin1234",
    # Strong
    "Tr0ub4dor&3",
    "C0mpl3x!Pass",
    "X#9mK@vL2qW!",
    "correct-horse-Battery-staple1!",
    "z$R8nP@2fLqW#mE7",
]

ITERATIONS = 100_000

def run():
    elapsed = timeit.timeit(
        lambda: [score_password(p) for p in PASSWORDS],
        number=ITERATIONS,
    )
    total = ITERATIONS * len(PASSWORDS)
    rate = total / elapsed

    print(f"Passwords in benchmark : {len(PASSWORDS)}")
    print(f"Iterations             : {ITERATIONS:,}")
    print(f"Total scored           : {total:,}")
    print(f"Elapsed                : {elapsed:.3f}s")
    print(f"Throughput             : {rate:,.0f} passwords/sec")

if __name__ == "__main__":
    run()
