import numpy as np
import cv2


l = [[[7,255,1],[0,246,0],[0,253,3],[0,255,0],[0,255,0],[0,255,0],[10,255,4],[8,246,3],[21,244,12],[23,245,9],[23,251,0],[16,253,0],[7,252,0],[0,255,0],[0,255,0],[0,255,0],[0,255,0],],
     [[20,255,10],[16,252,14],[0,226,4],[6,247,18],[2,255,0],[4,255,0],[0,248,0],[14,255,9],[11,247,9],[14,247,9],[18,251,0],[16,253,0],[9,253,0],[2,255,0],[0,255,0],[0,255,0],[0,255,0],],
     [[24,243,9],[26,235,23],[42,230,65],[27,216,47],[23,240,19],[26,255,9],[0,247,0],[0,255,0],[0,254,3],[0,251,7],[9,252,0],[14,252,0],[14,252,0],[9,254,0],[0,255,0],[0,255,0],[0,255,1],],
     [[38,234,22],[0,79,0],[0,54,0],[71,209,98],[33,201,28],[45,255,28],[0,251,0],[0,255,0],[0,255,0],[0,255,5],[0,254,0],[13,252,0],[20,251,0],[14,251,0],[0,254,0],[0,254,2],[0,255,2],],
     [[48,215,35],[0,68,0],[0,28,0],[0,39,0],[79,195,74],[50,223,35],[24,255,17],[0,255,0],[0,255,0],[0,255,0],[0,255,0],[9,253,0],[21,248,3],[20,247,6],[5,250,6],[0,252,5],[2,255,4],],
     [[85,225,78],[0,46,0],[216,255,240],[0,12,0],[0,42,0],[70,201,56],[19,235,16],[0,255,5],[0,255,0],[0,255,0],[0,255,0],[5,253,0],[20,246,7],[20,245,10],[7,249,6],[0,252,3],[2,255,4],],
     [[76,191,74],[0,35,0],[225,255,237],[237,255,245],[0,20,0],[0,45,0],[53,217,55],[15,242,31],[0,253,7],[0,255,0],[0,255,0],[0,255,0],[13,245,12],[14,244,13],[5,253,0],[0,255,0],[2,255,1],],
     [[78,180,79],[0,51,0],[236,255,242],[240,251,241],[248,255,235],[0,33,0],[0,46,0],[47,216,59],[13,236,30],[0,250,9],[0,255,0],[0,255,0],[7,247,12],[7,247,10],[2,255,0],[0,255,0],[2,255,0],],
     [[87,186,86],[0,32,0],[232,255,237],[236,249,235],[255,255,240],[248,255,230],[0,25,0],[0,49,0],[54,210,62],[31,231,36],[19,252,14],[0,240,0],[22,255,26],[6,255,11],[0,246,0],[10,255,0],[0,255,0],],
     [[97,199,91],[0,44,0],[201,244,211],[244,255,248],[237,239,220],[251,254,229],[250,255,235],[0,21,0],[0,37,0],[60,203,64],[46,241,37],[22,253,13],[0,244,0],[0,249,0],[12,255,6],[0,244,0],[0,255,0],],
     [[90,201,73],[0,39,0],[220,255,240],[239,255,254],[255,255,244],[249,240,220],[255,255,242],[235,237,217],[0,19,0],[0,45,0],[50,198,44],[40,237,27],[14,246,3],[0,250,0],[14,255,12],[1,255,2],[0,254,0],],
     [[87,206,68],[0,45,0],[209,255,233],[237,255,255],[255,255,247],[255,255,242],[255,242,234],[255,253,252],[237,240,245],[0,13,0],[0,47,0],[76,231,62],[47,246,30],[10,239,0],[0,233,0],[6,255,13],[0,253,2],],
     [[79,204,64],[0,65,0],[190,239,217],[239,254,255],[240,237,232],[255,255,245],[255,255,248],[249,232,236],[255,247,255],[243,255,255],[0,32,0],[0,46,0],[84,235,66],[34,227,23],[26,254,31],[0,242,4],[0,251,5],],
     [[70,196,60],[0,46,0],[221,255,247],[243,252,255],[255,252,251],[255,255,249],[235,226,222],[255,253,255],[254,241,255],[233,233,247],[246,255,240],[0,37,0],[0,46,0],[62,218,57],[43,253,51],[0,237,5],[2,251,5],],
     [[77,201,78],[0,38,0],[227,255,245],[248,252,255],[248,238,244],[255,254,255],[251,255,255],[233,240,243],[250,251,255],[253,252,255],[255,255,252],[250,255,238],[0,41,0],[0,57,0],[3,200,14],[13,253,22],[2,251,5],],
     [[72,203,88],[0,37,0],[227,255,245],[250,253,255],[252,244,245],[255,255,252],[236,244,243],[241,255,254],[246,255,255],[251,250,252],[255,253,254],[254,246,239],[236,255,244],[0,34,0],[40,229,48],[17,255,20],[2,252,3],],
     [[57,204,92],[0,38,0],[217,255,244],[238,245,248],[255,255,245],[255,255,242],[240,247,244],[244,255,255],[248,255,251],[255,255,245],[255,255,244],[255,249,240],[237,255,255],[0,30,0],[26,214,31],[0,244,0],[2,253,2],],
     [[52,182,75],[0,59,0],[223,255,251],[248,254,255],[233,228,213],[255,255,244],[251,252,255],[233,242,246],[0,4,0],[0,10,0],[14,28,0],[3,33,0],[0,19,0],[0,41,0],[27,241,34],[9,255,7],[0,254,0],],
     [[120,203,101],[0,28,0],[226,247,245],[250,249,255],[255,255,254],[16,8,8],[255,247,255],[247,245,255],[243,254,251],[0,18,0],[120,194,88],[76,187,51],[50,200,63],[27,230,55],[0,242,0],[0,255,0],[0,255,0],],
     [[129,204,88],[0,53,0],[218,255,233],[228,255,251],[0,14,0],[0,11,0],[0,0,6],[251,249,255],[242,255,255],[0,37,0],[0,53,0],[62,228,43],[36,245,47],[3,252,23],[0,255,0],[0,255,0],[0,255,0],],
     [[85,194,42],[0,63,0],[161,255,177],[0,53,0],[0,47,0],[102,189,91],[0,25,0],[235,249,247],[237,254,255],[198,254,219],[0,55,0],[63,254,57],[0,227,1],[0,243,0],[1,255,0],[0,254,0],[0,255,0],],
     [[64,222,28],[0,77,0],[0,90,0],[38,223,59],[46,230,40],[81,231,64],[0,36,0],[0,21,0],[222,255,247],[207,255,234],[0,58,0],[27,229,28],[4,243,10],[14,255,14],[8,254,0],[0,244,0],[4,254,0],],
     [[37,255,16],[3,233,0],[2,252,19],[0,253,13],[0,233,0],[43,255,27],[76,214,66],[0,37,0],[206,255,227],[195,255,217],[0,60,0],[46,244,49],[0,221,5],[11,241,10],[29,244,9],[41,255,19],[9,251,2],],
     [[3,251,0],[1,255,0],[0,255,0],[0,255,0],[2,255,0],[6,247,0],[46,225,40],[75,212,74],[0,46,0],[0,64,0],[46,225,46],[14,223,13],[22,248,29],[23,251,26],[16,233,4],[21,244,5],[7,251,3],],
     [[11,255,0],[6,255,0],[0,255,0],[0,255,0],[0,255,0],[11,250,9],[32,234,33],[45,227,43],[48,226,37],[43,233,24],[27,246,5],[13,251,0],[2,248,10],[0,248,13],[0,250,7],[0,253,3],[2,255,4],],
]

if __name__ == "__main__":
    np.set_printoptions(threshold=np.inf)
    l = np.array(l)
    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            p = l[i, j, :]
            if p[0]+p[1]+p[2] > 600:
                l[i, j, :] = [255,255,255]
            if p[0]+p[1]+p[2] < 100:
                l[i, j, :] = [0, 0, 0]
            if p[1] > p[2]+p[0]:
                l[i, j, :] = [0, 255, 0]

    for i in range(l.shape[0]):
        for j in range(l.shape[1]):
            p = l[i, j, :]
            if [p[0],p[1],p[2]] != [255,255,255] and [p[0],p[1],p[2]]!= [0, 0, 0] and [p[0],p[1],p[2]]!=[0, 255, 0]:
                l[i, j, :] = [0,0,0]


    #print(l)
    cv2.imwrite("Images/hello.jpg", l)

    #
    #
    # f1 = lambda p: [255,255,255] if p[0]+p[1]+p[2] > 600 else p
    # f2 = lambda p: [0,0,0] if p[0]+p[1]+p[2] < 100 else p
    # f3 = lambda p: [0,255,0] if p[1] > p[2]+p[0] else p
    # print(f3(f2(f1(l))))