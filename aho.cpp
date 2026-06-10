#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <string>
#include <algorithm>
#include<set>
using namespace std;
struct Node {
    map<char, int> next;
    int link = -1;
    vector<string> output;
};
vector<Node> trie(1);
void insert(string s, string type) {
    int node = 0;
    for (char c : s) {
        if (!trie[node].next.count(c)) {
            trie[node].next[c] = trie.size();
            trie.push_back(Node());
        }
        node = trie[node].next[c];
    }
    trie[node].output.push_back(type); 
}
void build() {
    queue<int> q;
    trie[0].link = 0;
    for (auto &p : trie[0].next) {
        q.push(p.second);
        trie[p.second].link = 0;
    }
    while (!q.empty()) {
        int v = q.front(); q.pop();
        for (auto &p : trie[v].next) {
            char c = p.first;
            int u = p.second;
            int j = trie[v].link;
            while (j && !trie[j].next.count(c)) {
                j = trie[j].link;
            }
            if (trie[j].next.count(c))
                j = trie[j].next[c];
            trie[u].link = j;
            for (auto &x : trie[j].output) {
                trie[u].output.push_back(x);
            }           
            q.push(u);
        }
    }
}
vector<string> search(string text) {
    int node = 0;
    set<string> found;
    for (char c : text) {
        while (node && !trie[node].next.count(c))
            node = trie[node].link;
        if (trie[node].next.count(c))
            node = trie[node].next[c];
        for (auto &type : trie[node].output)
            found.insert(type); 
    }
    return vector<string>(found.begin(), found.end());
}
string toLower(string s) {
    for (char &c : s) c = tolower(c);
    return s;
}
int main() {
    insert("or 1=1", "SQL Injection");
    insert("<script>", "XSS");
    insert("union select", "SQL Injection");
    insert("drop table", "SQL Injection");
    //insert("select *", "SQL Injection");
    insert("alert", "XSS");
    insert("exec", "Command Injection");
    insert("cmd=", "Command Injection");
    insert("--", "SQL Injection");
    insert("delete from", "SQL Injection");
    insert("rm -rf", "Command Injection");
    insert("' or", "SQL Injection");
    insert("and '1'='1", "SQL Injection");
    insert("or true", "SQL Injection");
    insert("and true", "SQL Injection");
    insert("or false", "SQL Injection");
    insert("and false", "SQL Injection");
    insert("or 1=2", "SQL Injection");
    insert("and 1=1", "SQL Injection");
    insert("\" or \"1\"=\"1", "SQL Injection");//LOGIN BYPASS VARIANTS
    insert("'='", "SQL Injection");
    insert("' like '", "SQL Injection");
    insert("' or ''='", "SQL Injection");
    insert("\" or \"\"=\"", "SQL Injection");
    insert("../", "Path Traversal");
    insert("<img", "XSS");
    insert("waitfor delay", "SQL Injection");
    insert("set-cookie", "Header Injection");
    insert("include file", "File Inclusion");
    insert("file=", "File Inclusion");
   // insert("injected_param", "Injection");
    insert("%3cscript", "XSS");
    insert("%2f%2a", "SQL Injection");//ENCODING / OBFUSCATION VARIANTS
    insert("%2a%2f", "SQL Injection"); 
    insert("%23", "SQL Injection");     
    insert("%2d%2d", "SQL Injection");   
    insert("%27", "Encoding Attack");
    insert("%22", "Encoding Attack");
    insert("#", "SQL Injection");
    insert("%3e", "Encoding Attack");
    insert("/*!union*/", "Obfuscated SQL Injection");
    insert("union/**/select", "SQL Injection");
    insert("union%0aselect", "SQL Injection");
    insert("union%09select", "SQL Injection");
    insert("concat(", "SQL Injection");
    insert("char(", "SQL Injection");
    insert("information_schema", "SQL Injection");
    insert("load_file", "File Inclusion");
    insert("0x53 0x45 0x4C", "Hex Encoded SQL Injection");
    insert("%20union%20select", "Encoded SQL Injection"); 
    insert("union all select", "SQL Injection"); 
    insert("document.cookie", "XSS");
    insert("onerror", "XSS");
    insert("onload", "XSS");
    insert("xp_cmdshell", "SQL Injection"); 
    insert("benchmark(", "SQL Injection");       
    insert("load data infile", "File Inclusion"); 
    insert("system(", "Command Injection");
    insert("powershell", "Command Injection"); 
    insert("union distinct select", "SQL Injection"); 
    insert("group_concat(", "SQL Injection"); 
    insert("hex(", "SQL Injection"); 
    insert("sleep(", "SQL Injection"); // already added, but keep variants
    insert("wget", "Command Injection"); 
    insert("curl", "Command Injection"); 
    insert("etc/passwd", "Path Traversal"); 
    insert("c:\\windows\\system32", "Path Traversal"); 
    insert("#", "SQL Injection");
    insert("/*", "SQL Injection");
    insert("*/", "SQL Injection");
    insert("if(", "SQL Injection");
    insert("case when", "SQL Injection");//TIME-BASED BLIND SQLi
    insert("pg_sleep(", "SQL Injection");
    insert("waitfor time", "SQL Injection");
    build();
    string input;
    cout << "Enter query: ";
    getline(cin, input);
    input = toLower(input);
    vector<string> result = search(input);
    if (!result.empty()) {
        cout << "\nMalicious detected!\n";
        cout<<"\n Detected Attack Types:\n" ;
        for (auto &r : result)
            cout << "- " << r << endl;
    }
    else 
    cout << "Safe input" << endl;
    return 0;
}