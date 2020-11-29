def top_sort(graph):
    #初始化所有顶点入度为0  
    in_degrees = [0 for _ in range(len(graph))]
    #计算每个顶点的入度
    n = len(graph)
    for u in range(n):
        for v in graph[u]:
            in_degrees[v] += 1
    # 筛选入度为0的顶点
    Q = [u for u in in_degrees if in_degrees[u] == 0]
    top_seq = []
    while Q:
        u = Q.pop()
        top_seq.append(u)
        for v in graph[u]:
            #移除其所有出边
            in_degrees[v] -= 1
      		# 遇到出度为 0 的节点， 加入删除队列 
            if not in_degrees[v]:
                Q.append(v)
    # 检查是否有效
    if len(top_seq) == len(in_degrees):
        return top_seq
    else:
        return None
if __name__ == '__main__':
    # G 为边表， G[i] 表示从 i 出发 鞥一步到达的点 ！
    G = [
        [1,2,3],
        [4],
        [1],
        [2,4],
        [],
    ]
    print(top_sort(G))