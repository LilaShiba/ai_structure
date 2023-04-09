import numpy as np
import pandas as pd
import collections 
import matplotlib as plt 



class Jiji():

    def __init__(self, x, name):
        '''
            Takes in a 1D Vector
        '''
        self.vector = np.array(x)
        self.name = name
        
        c = collections.Counter(self.vector)
        self.dict = c
        self.vals, self.cnt = list(zip(*c.items()))
        self.n = np.sum(self.cnt)
        self.probVector = [x/self.n for x in self.cnt]
        self.mu = np.mean(self.cnt)
        self.basic_stats()

    def basic_stats(self):
        self.get_entropy()
        self.get_variance()
        self.get_pdf_linear_binning()
        self.get_pdf_log_binning()
        # resets values to og scale :)
        self.pdf()
        
    def get_entropy(self):
    
        h = collections.defaultdict(int)
        
        for node in self.vector:
            h[node] += 1
        p = []
        for x in h.keys():
           p.append((h[x] / self.n))

        self.p = p
        self.entropy = round(-np.sum(p * np.log2(p)),2)
        print(self.entropy)
        return self.entropy
    
    def get_variance(self):
        self.variance = np.sum([(x - self.mu)**2 for x in self.vector]) / self.n
        return self.variance
    
    def get_norm_vector(self,x=False):
        if not x:
            x = self.vector
        v_min = np.min(x)
        v_max = np.max(x)
        v_max_min = v_max - v_min
        self.vector_norm = [(x-v_min)/(v_max_min) for x in x]
        return self.vector_norm



    # Internal Use Only
    def pdf(self):
        counter = collections.Counter(self.vector)

        self.dict = counter
        self.vals, self.cnt = zip(*counter.items())
        self.mu = np.mean(self.cnt)
        self.n = np.sum(self.cnt)
        self.probVector = [x/self.n for x in self.cnt]

    def get_ctl(self, samples=1000):
        res = []
        n = len(self.vector)-1

        for dataPoint in range(samples):
            idxVector = [ 
                        self.vector[np.random.randint(0,n)], 
                        self.vector[np.random.randint(0,n)],
                        self.vector[np.random.randint(0,n)]
                        ]
            rs = np.sum(idxVector) // len(idxVector)
            res.append(rs)
        plt.hist(res)
        plt.show()
        self.ctl_values = np.histogram(rs)
    
    def get_cdf(self,show=True):
        values = np.array(self.probVector)
        cdf = values.cumsum() / values.sum()
       # cdf = np.cumsum(probVector)
        self.ccdf = 1-cdf
        self.cdf = cdf 
        if show:
            plt.xscale("log")
            plt.yscale("log")
            plt.title(f"Cumulative Distribution")
            plt.ylabel("P(K) >= K")
            plt.xlabel("K")
            plt.plot(cdf[::-1])
            plt.show()

    def get_pdf_linear_binning(self):
        if not self.probVector:
            self.pdf(self.vector)
        plt.xlabel('K')
        plt.ylabel('P(K)')
        plt.plot(self.vals, self.probVector,'o')
        plt.show()
    
    def get_pdf_log_binning(self,show=True):
        if not self.probVector:
            self.pdf(self.vector)

        inMax, inMin = max(self.probVector), min(self.probVector)
        self.logBins = np.logspace(np.log10(inMin),np.log10(inMax))
        # degree, count
        self.hist_cnt, self.log_bin_edges = np.histogram(self.probVector,bins=self.logBins,
                                    density=True, range=(inMin, inMax))
       
        n = np.sum(self.hist_cnt)

        self.log_prob_vector = [x/n for x in self.hist_cnt]

        if show:
            plt.title(f"Log Binning & Scaling")
            plt.xscale("log")
            plt.yscale("log")
            plt.xlabel('K')
            plt.ylabel('P(K)')
            plt.plot(self.hist_cnt, self.log_prob_vector[::-1], 'o')
            plt.show()

    def get_pdf_from_mu(self, idx=-1):
        '''        
        f(x) = (1/σ√(2π)) * e^(-(x-μ)²/(2σ²))

        Where:

        x is the value of the random variable
        μ is the mean of the distribution
        σ is the standard deviation of the distribution
        e is the mathematical constant e ≈ 2.71828
        
        '''
        c = collections.Counter(self.vector)
        self.dict = c
        self.vals, self.cnt = zip(*c.items())
        self.n = np.sum(self.cnt)
        self.mu = self.n/len(self.cnt)
        self.probVector = [x/self.n for x in self.cnt]
        if idx >-1:
            print("PDF_VALUE:", self.probVector[idx])

    def get_coverance(self,v2):
        n = len(self.vector)
        y_mu = np.mean(v2)
        coverance = np.sum([(x - self.mu)*(y - y_mu) 
                            for x,y in zip(self.vector,v2)]) / n-1
        return coverance
    
    def get_slope(self,v2):
        slope = self.get_coverance(v2) / self.get_variance()
        self.slope = slope
        return slope

    def linear_regression(self, n2):
         # y_hat = w.X + b
        
        x_mu = self.mu
        y_mu = n2.mu
        

        top_term = 0
        btm_term = 0

        for i in range(n):
            top_term += (self.vector[i] - x_mu) * (n2.vector[i] - y_mu)
            btm_term += (self.vector[i] - x_mu)**2

        m = top_term/btm_term
        b = y_mu - (m * x_mu)

        
        print (f'm = {m} \nb = {b}')


        max_x = np.max(self.x) + 10
        min_x = np.min(self.y) - 10
        x_delta = np.linspace (min_x, max_x, 10)

        y_delta = b + m * x_delta

        plt.scatter(self.x,self.y)
        plt.plot(x_delta,y_delta,'ro')
        plt.show()
        return y_delta              

    def knn_init(self):
        self.create_node_list()
        self.create_graph()

    def create_node_list(self, p2):
        x,y = self.vector, p2.y
        nodeList = [] 
        adjList = collections.defaultdict()
        
        for idx in range(self.n-1):
            dx = self.vector[idx]
            dy = p2.vector[idx]
            delta = node(   dx, 
                            dy,
                            idx,
                            self.label         
                        )
            nodeList.append(delta)
            adjList[(dx,dy)] = delta
        
        self.nodeList = nodeList
        self.adjList = adjList
    
    def create_graph(self):
            
        graph = collections.defaultdict(list)

        for node in self.nodeList:
            x,y = node.x, node.y 
            graph[(x,y)].append(node)
        
        delta = list(graph.keys())
        x = [i[0] for i in delta]
        y = [i[1] for i in delta]
        self.scatterGraph = (x,y)
        self.graph = graph
    
    def simple_knn(self,target=False,knnSize=5):
        # preprocess
        self.knn_init()
        self.distanceVector = collections.defaultdict()
        cord_vector = list(self.graph.values())
        x_y = [(p.x,p.y) for p in self.nodeList]
        x,y = zip(*x_y)
        fig, ax = plt.subplots()

        ax.scatter(x, y, s = 10)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        fig.set_size_inches(20, 20)
        plt.show()

    # Begin NPL Helpers
    def freq_count(self,path):
        with open(path, 'r') as file:
            book = file.read()
            file.close()

        char_freq = collections.Counter(book.lower())
        filtered_keys = sorted( 
            [(key,val) for key,val in char_freq.items() if key.isalpha()]
            , key=lambda x:x[1]
            )

        x,y = zip(*filtered_keys)

        n = np.sum(y)
        probVector = zip(x, [cnt/n for cnt in y])
        px,py = zip(*probVector)
        
        mu = np.mean(y)

        plt.xlabel('Char')
        plt.ylabel('Frequency')
        plt.title('Frequency of Char')
        plt.scatter(x, y)
        plt.show()


        plt.xlabel('K')
        plt.ylabel('P(K)')
        plt.title('Prob Vector')
        plt.scatter(px, py)
        plt.show()



        return probVector, mu, filtered_keys

class node():
    
    def __init__(self,x,y,idx,label) -> None:
        self.x = x 
        self.y = y 
        self.idx = idx
        self.label = label