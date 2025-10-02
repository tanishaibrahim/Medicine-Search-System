import json
import sys
from main import search_medicines

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("   python submission.py [prefix|substring|fulltext|fuzzy]           -> run benchmark queries")
        print("   python submission.py [prefix|substring|fulltext|fuzzy] <query1> <query2> ...   -> run one or more queries")
        sys.exit(1)

    mode = args[0].lower()
    if mode not in ["prefix", "substring", "fulltext", "fuzzy"]:
        print("Invalid mode! Use one of: prefix, substring, fulltext, fuzzy")
        sys.exit(1)

   
    if len(args) >= 2:
        queries = args[1:]  
        results_dict = {}

        for idx, query in enumerate(queries, start=1):
            query = query.strip()  
            matches = search_medicines(query, mode)
            results_dict[str(idx)] = matches
            print(f"Processed query {idx}: {query}")

        output = {"results": results_dict}

        
        with open("submission.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        
        print("\n" + json.dumps(output, indent=4, ensure_ascii=False))
        print("\n submission.json generated successfully for multiple queries!")
        return

    
    try:
        with open("benchmark_queries.json", "r", encoding="utf-8") as f:
            benchmark = json.load(f)
    except FileNotFoundError:
        print(" benchmark_queries.json not found in current directory!")
        sys.exit(1)

    results_dict = {}
    for qid, query_text in benchmark.items():
        query_text = query_text.strip()
        matches = search_medicines(query_text, mode)
        results_dict[str(qid)] = matches
        print(f"Processed benchmark query {qid}: {query_text}")

    output = {"results": results_dict}

    with open("submission.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"\n submission.json generated successfully for batch queries using {mode} search!")

if __name__ == "__main__":
    main()
