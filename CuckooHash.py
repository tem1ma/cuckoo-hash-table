#I hereby certify that this program is solely the result of my own work 
#and is in compliance with the Academic Integrity policy of the course syllabus 
#and the academic integrity policy of the CS department.

import random
from BitHash import *

class Pair(object):
    def __init__(self, k, d):
        self.key = k
        self.data = d    


class CuckooHashTab(object):
    def __init__(self, size=1):
        self.__hashArray1 = [None] * size
        self.__hashArray2 = [None] * size
        self.__numKeys = 0
        
    # return current number of keys in table    
    def __len__(self): return self.__numKeys
    
    #returns the size of the hash table
    def hashSize(self):
        return len(self.__hashArray1)
    
    #this method returns None if there are no remaining ejected residents upon completion
    #otherwise returns the last ejected resident
    def __insert(self, p, hashTab1, hashTab2):
        # hash in order to identify which nest to insert the key into
        hash0 = BitHash(p.key,0)
        hash1 = BitHash(p.key,hash0)
        nest1 = hash0 % len(hashTab1)
        nest2 = hash1 % len(hashTab2)        
        
        #if there is nothing in nest 1, set it to equal p
        if hashTab1[nest1]==None:
            hashTab1[nest1] = p
            
            return None     #successful insertion
        
        #otherwise, check if the appropriate nest in hashtab 2 is empty, and insert p there    
        elif hashTab2[nest2]==None:
            hashTab2[nest2] = p
            
            return None    #successful insertion   
        
    
        #if both are occupied, kick out the first position
        #get the key,data pair that already resides there
        resident1=hashTab1[nest1]
        #set that position to equal the new pair
        hashTab1[nest1]=p
        
        
        #move the prexisting key,data pair to it's position in the 2nd table
        for i in range(50):
            #find the position where the kicked out resident1 of table 1 should be 
            #moved to in table 2
            hash0 = BitHash(resident1.key, 0)
            hash1 = BitHash(resident1.key, hash0)
            nest2 = hash1 % len(hashTab2)   #this is where the evicted resident1 should go   
            
            #store the resident that already exists at that position
            resident2=hashTab2[nest2]
            #insert resident1 into that position in table2
            hashTab2[nest2]=resident1
            
            #if nothing was displaced (ie resident 2 was None), insertion has been completed
            if not resident2: 
                return None
            
        
            #find the position where the kicked out resident2 of table 2 should be 
            #moved to in table 1 
            hash0 = BitHash(resident2.key, 0)
            nest1 = hash0 % len(hashTab1)   #this is where the evicted resident2 should go      
            
            #get the resident that already exists at that position
            resident1=hashTab1[nest1] 
            #insert resident2 into that position in table1
            hashTab1[nest1]=resident2
            
            #if nothing was displaced, insertion has been completed    
            if not resident1: 
                return None
            #otherwise, loop again
            
                   
        #if we made it to this point, it means no empty spot was found, and resident1 was last evicted
        return resident1
    
    
    #returns True if successfully inserted, otherwise returns False
    def insert(self, k, d):
        
        #create a new key,data pair
        p=Pair(k,d)         
        #if the key is already there, return false
        nest1, p1 = self.__findNest1(k)     #returns p1 if p1.key==k, else returns false
        nest2, p2 = self.__findNest2(k)     #returns p2 if p2.key==k, else returns false
        if p1: return False
        elif p2: return False
        
        #try to insert the key,data pair into hashArray1 or 2. LastPair should be None if successful
        #otherwise it's the last key,data pair that was ejected from HashArr1
        lastPair=self.__insert(p,self.__hashArray1,self.__hashArray2)
        
        #if self.__insert returned None, the key,data pair was successfully inserted
        if not lastPair: 
            self.__numKeys+=1
            # if the tables are getting too full (the number of keys equals half the table size), grow the tables
            if self.__numKeys > len(self.__hashArray1)*.5: self.__growHash()              
            return True    #if there were no remaining residents to insert, everything has been successfully inserted
        
        
    
        #else: deal with resident 1
        #grow the tables and reset bithash
        self.__growHash() 
        
        #try doing another insert now that we've grown the tables
        lastPair=self.__insert(lastPair, self.__hashArray1,self.__hashArray2)
        #if we successfully inserted
        if not lastPair: 
            self.__numKeys+=1
            return True
        print("ejected last pair:",len(lastPair.key), "tried to insert:", len(k))
        return False
               
    
    
    #grows the two hash tables when they get too full
    def __growHash(self):
        #reset the hash function
        ResetBitHash()
        
        #create a new list 2x the size of the orig _hashArray
        newList1= [None] * len(self.__hashArray1) * 2   
        newList2= [None] * len(self.__hashArray2) * 2
        
        #for every nest containing a key,data pair in hasharray 1, rehash it and
        #insert it into a new, longer list
        #insert using the __insertion method to deal with any possible collisions
        for nest in self.__hashArray1:
            #if the nest is not empty
            if nest:
                #try inserting it into the new lists
                #lastPair will be None if successfully inserted, otherwise will be
                #the last resident that was evicted
                lastPair=self.__insert(nest, newList1, newList2)
                
                if lastPair: 
                    #raise IndexError(lastPair.key, "was evicted")
                    print(len(lastPair.key), "was evicted from newList1")
                    
        
        #repeat for hash table 2
        for nest in self.__hashArray2:
            if nest: 
                lastPair=self.__insert(nest, newList1, newList2)
                
                if lastPair: 
                    print(len(lastPair.key), "was evicted from newList2")
                    #raise IndexError(lastPair.key, "was evicted")
                    
                
        #make hash table 1 and 2 now point to the new, longer lists        
        self.__hashArray1=newList1
        self.__hashArray2=newList2
        
    
    
    def __findNest1(self, k):
        # hash in order to identify the nest where the key might be
        hash0 = BitHash(k,0)
        nest1 = hash0 % len(self.__hashArray1)
        
        #extract the key data pairs from those positions in the respective hash tables
        p1=self.__hashArray1[nest1]  
        
        #if the key is in the first hash table, return the nest where it was found
        #and the key
        if p1 and p1.key==k:
            return nest1, p1
        else: return nest1, None
        
    def __findNest2(self, k):
        # hash (using the second hash function) in order to identify the nest where the key might be
        hash0 = BitHash(k,0)
        hash1 = BitHash(k,hash0)
        nest2 = hash1 % len(self.__hashArray2)
        
        #extract the key data pairs from that position in the 2nd hash table
        p2=self.__hashArray2[nest2]     
        
        #if the key is in the first hash table, return the nest where it was found
        #and the key
        if p2 and p2.key==k:
            return nest2, p2  
        else: return nest2, None
    
    def find(self, k):
        nest1, p1 = self.__findNest1(k)
        nest2, p2 = self.__findNest2(k)
        if p1:
            return p1.data
        elif p2:
            return p2.data
        else: return None
        
    
    def delete(self, k):
        # hash in order to identify the nest where the key might be
        hash0 = BitHash(k,0)
        hash1 = BitHash(k,hash0)
        
        nest1 = hash0 % len(self.__hashArray1)
        nest2 = hash1 % len(self.__hashArray2)
        
        #extract the key data pairs from those positions in the respective hash tables
        p1=self.__hashArray1[nest1]
        p2=self.__hashArray2[nest2]
        
        #if there is a key, and the key is in the first hash table, set that position equal to None
        if p1 and p1.key==k:
            self.__hashArray1[nest1]=None
            self.__numKeys-=1
            return p1.data
        
        #else if it's in the second hash table, set the position equal to None
        elif p2 and p2.key==k:
            self.__hashArray2[nest2]=None
            self.__numKeys-=1
            return p2.data            
        
        #if the key was never there to begin with, return None 
        else: return None


   

def __main():
    c=CuckooHashTab()
    print(c.insert("apple", 1))
    print(c.insert("banana", 2))
    print(c.insert("cherry", 3))
    print(c.insert("date", 4))
    print(c.insert("elderberry", 5))
    print(c.insert("fig", 6))
    print(c.insert("grape", 7))
    print(c.insert("huckleberry", 8))
    print(c.insert("jackfruit", 9))
    print(c.insert("kiwi", 10))
    print(c.insert("lime", 11))
    print(c.insert("mango", 12))
    print(c.insert("nectarine", 13))
    print(c.insert("orange", 14))
    print(c.insert("pineapple", 15))
    print(c.insert("quince", 16))
    print(c.insert("raspberry", 17))
    print(c.insert("strawberry", 18))
    print(c.insert("tangerine", 19))
    print(c.insert("watermelon", 20))       

        
#if __name__ == '__main__':
    #__main() 