from bisect import bisect_right

class Interpolate:
    def __init__(self, x_list, y_list):
        if any(y - x <= 0 for x, y in zip(x_list, x_list[1:])):
            raise ValueError("x_list must be in strictly ascending order!")
        self.x_list = x_list
        self.y_list = y_list
        self.y_list[0]=0
        intervals = zip(x_list, x_list[1:], y_list, y_list[1:])
        self.slopes = [(y2 - y1) / (x2 - x1) for x1, x2, y1, y2 in intervals]

    def __call__(self, x):
        if x ==0:
            return 0
        if not (self.x_list[0] <= x ):
            raise ValueError("x out of bounds!")
        if x == self.x_list[-1]:
            return self.y_list[-1]
        if x > self.x_list[-1]:
            return self.y_list[-1] + self.slopes[-1] *(x-self.x_list[-1] )
        i = bisect_right(self.x_list, x) - 1
        return self.y_list[i] + self.slopes[i] * (x - self.x_list[i]) 
        
#10senkrecht
x = [0,1,2,3,4,5,6,7,8,9,10,13,16,19,22,25,28,31,34,37,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,300,325,350,375,400,425,450,475,500,525,550,575,600,650]
senkrecht10 = [[6,7,8,8,10,11,12,12,13,14,16,17,18,19,20,22,23,23,24,25,26,28,30,31,32,34,36,37,38,40,42,43,46,49,52,55,58,61,64,67,70,73,76,79,82,85,88,91,94,97,103,110,118,126,133,140,148,156,163,170,178,186,193,208],
[20,7,8,10,11,12,13,14,16,17,18,20,23,24,26,28,29,30,31,32,34,36,38,40,42,44,46,48,50,52,54,56,59,62,67,71,76,80,84,89,92,97,102,106,110,114,119,124,127,132,136,145,156,167,178,188,199,210,221,232,242,253,264,275,296],
[30,8,11,12,14,16,18,19,22,23,25,28,30,32,35,36,38,40,42,43,46,48,52,54,58,60,64,66,70,72,76,78,82,88,94,100,106,112,118,124,130,136,142,148,154,160,166,172,178,184,190,202,216,232,246,262,276,292,306,322,336,352,366,382,412],
[40,10,12,14,17,19,22,24,26,29,31,35,38,42,44,48,50,53,55,58,60,65,68,73,77,82,85,90,94,98,102,107,110,119,127,136,144,152,161,169,178,186,194,203,211,220,228,236,245,253,262,278,300,320,342,362,384,404,426,446,468,488,510,530],
[50,11,14,17,20,23,26,29,32,35,38,43,48,53,58,61,65,70,73,77,82,88,95,101,108,114,121,127,134,140,148,154,161,174,187,200,214,227,240,253,266,280,293,306,319,332,346,359,372,385,398,425,457,491,523,577],
[60,12,16,19,23,26,30,34,37,41,44,52,58,65,71,77,83,89,94,100,106,115,125,134,144,154,163,173,182,192,202,211,221,240,259,278,298,317,336,355,374,394,413,432,451,470,490,509],
[70,13,18,23,28,32,37,42,47,52,56,66,77,86,95,103,110,118,125,133,140,154,166,179,191,204,216,229,241,254,266,280,292,317,342,367,392,418,443,468,493,518,544],
[80,14,20,26,32,38,44,50,56,62,68,82,96,109,120,130,139,149,157,167,176,192,208,223,239,254,270,286,301,317,332,348,364,395,426,457,488,520]]
aw10s = []
for y in senkrecht10:
    aw10s.append( Interpolate(x[:len(y)], y) )

#10wagerecht
x = [0,1,2,3,4,5,6,7,8,9,10,13,16,19,22,25,28,31,34,37,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,300,325,350,375,400,425,450,475,500,525,550,575,600,650,700,750,800]
waagerecht10 = [[10,5,6,7,7,8,9,10,10,11,12,13,14,15,16,17,18,19,19,20,21,22,23,25,26,27,28,30,31,32,33,35,36,38,41,43,46,48,51,53,56,58,61,63,66,68,71,73,76,78,81,86,92,98,105,111,117,123,130,136,142,148,155,161,173,186,198,211],
[20,6,7,8,9,10,11,12,13,14,15,17,19,20,22,23,24,25,26,27,28,30,32,33,35,37,39,40,42,44,45,47,49,52,56,59,63,67,70,74,77,81,85,88,92,95,99,103,106,110,113,121,130,139,148,157,166,175,184,193,202,211,220,229,247,265,283,301],
[30,7,9,10,12,13,15,16,18,19,21,23,25,27,29,30,32,33,35,36,38,40,43,45,48,50,53,55,58,60,63,65,68,73,78,83,88,93,98,103,108,113,118,123,128,133,138,143,148,153,158,168,180,193,205,218,230,243,255,268,280,293,305,318,343,368,393,418],
[40,8,10,12,14,16,18,20,22,24,26,29,32,35,37,40,42,44,46,48,50,54,57,61,64,68,71,75,78,82,85,89,92,99,106,113,120,127,134,141,148,155,162,169,176,183,190,197,204,211,218,232,250,267,285,302,320,337,355,372,390,407,425,442],
[50,9,12,14,17,19,22,24,27,29,32,36,40,44,48,51,54,58,61,64,68,73,79,84,90,95,101,106,112,117,123,128,134,145,156,167,178,189,200,211,222,233,244,255,266,277,288,299,310,321,332,354,381,409,436,464],
[60,10,13,16,19,22,25,28,31,34,37,43,48,54,59,64,69,74,78,83,88,96,104,112,120,128,136,144,152,160,168,176,184,200,216,232,248,264,280,296,312,328,344,360,376,392,408,424],
[70,11,15,19,23,27,31,35,39,43,47,55,64,72,79,86,92,98,104,111,117,128,138,149,159,170,180,191,201,212,222,233,243,264,285,306,327,348,369,390,411,432,453],
[80,12,17,22,27,32,37,42,47,52,57,68,80,91,100,108,116,124,131,139,147,160,173,186,199,212,225,238,251,264,277,290,303,329,355,381,407,433]]
aw10w = []
for y in waagerecht10:
    aw10w.append( Interpolate(x[:len(y)], y) )

#senkrecht12
x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,60,65,70,80,90,100]
senkrecht12 = [[10,6,7,8,10,11,12,13,13,14,16,16,17,17,18,18,19,19,20,20,22,22,23,24,24,25,25,26,26,28,28,28,29,29,30,30,31,31,32,32,34,34,35,35,36,36,37,37,38,38,40,40,40,41,42,42,46,48,52,58,64,70],
[20,7,10,11,13,14,16,17,18,19,20,22,23,24,25,26,28,29,30,31,32,34,35,35,36,37,38,38,40,41,42,42,43,44,46,46,47,48,49,49,50,52,53,53,54,55,56,56,58,59,60,60,61,62,64,64,68,73,78,86,96,104],
[30,8,11,13,16,18,20,22,24,25,28,29,31,32,35,36,38,40,42,43,46,47,48,49,50,52,53,54,55,56,58,59,60,61,62,64,65,66,67,68,70,71,72,73,74,76,77,78,79,80,82,83,84,85,86,88,94,100,106,118,130,142],
[40,11,14,17,20,23,25,28,30,32,35,37,40,42,44,47,49,52,54,56,59,61,62,65,66,68,70,72,73,76,77,79,80,83,84,86,88,90,91,94,95,97,98,101,102,104,106,108,109,112,113,115,116,119,120,122,131,140,149,167,18,203],
[50,12,17,20,25,29,32,35,38,41,44,47,50,53,56,59,62,65,68,71,74,77,79,82,84,86,89,91,94,96,98,101,103,106,108,110,113,115,118,120,122,125,127,130,132,134,137,139,142,144,146,149,151,154,156,158,170,182,194,218,242,266],
[60,12,17,22,26,31,35,38,42,46,49,53,56,60,64,67,71,74,79,82,85,89,91,95,97,101,103,107,109,113,115,119,121,125,127,131,133,137,139,143,145,149,151,155,157,161,163,167,169,173,175,179,181,185,187,191,205,221,235,265,295,325],
[70,13,19,25,31,37,42,46,50,54,59,62,67,71,76,79,84,88,92,96,101,104,108,112,115,119,122,126,130,133,137,140,144,148,151,155,158,162,166,169,173,176,180,184,187,191,194,198,202,205,209,212,216,220,223,227,245,263,281,317,353,389],
[80,14,23,30,38,46,52,56,62,67,73,78,83,88,92,97,102,107,111,116,121,126,131,136,140,145,150,155,160,164,169,174,179,184,188,193,198,203,208,212,217,222,227,232,236,241,246,251,256,260,265,270,275,280,284,289,313,337,361,409,457,505]]
aw12s = []
for y in senkrecht12:
    aw12s.append( Interpolate(x[:len(y)], y) )

#waagerecht12
x = [0,1,2,3,4,5,6,7,8,9,10,13,16,19,22,25,28,31,34,37,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,300,325,350,375,400,425,450,475,500,525,550,575,600,650,700,750,800]
waagerecht12 = [[10,6,7,8,8,10,11,12,12,13,14,16,17,18,19,20,22,23,23,24,25,26,28,30,31,32,34,36,37,38,40,42,43,46,49,52,55,58,61,64,67,70,73,76,79,82,85,88,91,94,97,103,110,118,126,133,140,148,156,163,170,178,186,193,208,223,238,253],
[20,7,8,10,11,12,13,14,16,17,18,20,23,24,26,28,29,30,31,32,34,36,38,40,42,44,46,48,50,52,54,56,59,62,67,71,76,80,84,89,92,97,102,106,110,114,119,124,127,132,136,145,156,167,178,188,199,210,221,232,242,253,264,275,296,318,340,361],
[30,8,11,12,14,16,18,19,22,23,25,28,30,32,35,36,38,40,42,43,46,48,52,54,58,60,64,66,70,72,76,78,82,88,94,100,106,112,118,124,130,136,142,148,154,160,166,172,178,184,190,202,216,232,246,262,276,292,306,322,336,352,366,382,412,442,472,502],
[40,10,12,14,17,19,22,24,26,29,31,35,38,42,44,48,50,53,55,58,60,65,68,73,77,82,85,90,94,98,102,107,110,119,127,136,144,152,161,169,178,186,194,203,211,220,228,236,245,253,262,278,300,320,342,362,384,404,426,446,468,488,510,530],
[50,11,14,17,20,23,26,29,32,35,38,43,48,53,58,61,65,70,73,77,82,88,95,101,108,114,121,127,134,140,148,154,161,174,187,200,214,227,240,253,266,280,293,306,319,332,346,359,372,385,398,425,457,491,523,577],
[60,12,16,19,23,26,30,34,37,41,44,52,58,65,71,77,83,89,94,100,106,115,125,134,144,154,163,173,182,192,202,211,221,240,259,278,298,317,336,355,374,394,413,432,451,470,490,509],
[70,13,18,23,28,32,37,42,47,52,56,66,77,86,95,103,110,118,125,133,140,154,166,179,191,204,216,229,241,254,266,280,292,317,342,367,392,418,443,468,493,518,544],
[80,14,20,26,32,38,44,50,56,62,68,82,96,109,120,130,139,149,157,167,176,192,208,223,239,254,270,286,301,317,332,348,364,395,426,457,488,520]]
aw12w = []
for y in waagerecht12:
    aw12w.append( Interpolate(x[:len(y)], y) )

if __name__ == '__main__' :
    print(aw10s[1](7)) 
    print(aw12w[7](686)) 