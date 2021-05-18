from block_kit import *
import json

# from benchmarkit import benchmark, benchmark_run

# SAVE_PATH = "/tmp/benchmark_time.jsonl"


# @benchmark(num_iters=100, save_params=True)
# def search_in_list(num_items=N):
#    for x in range(0, 10000):
m = Message(
    Blocks(
        Header(
            PlainText("test"),
        ),
        Section(
            PlainText("test"),
        ),
        Section(
            Fields(
                MarkDown("test"),
            ),
        ),
        Divider(),
        Image(
            ImageURL("https://via.placeholder.com/200x100"),
            AltText("alt"),
        ),
        Actions(
            Elements(
                Button(
                    PlainText("Create case"),
                    ActionId("actionId-0"),
                    Value("click me"),
                ),
                Button(
                    PlainText("Create case"),
                    ActionId("actionId-0"),
                    Value("click me"),
                ),
            ),
        ),
    ),
)

print(json.dumps(m, indent=4))

"""
benchmark_results = benchmark_run(
    [search_in_list],
    SAVE_PATH,
    comment="initial benchmark search",
)

"""
