import GetFisherVector
import GetMatchResult
import MatchFunM

if __name__ == '__main__':
    f_name = 'pos_leave.txt'
    f = open(f_name,'r')
    for line in f:
        v_name = line[0:-1]
        tmp = [(v_name,'gggg'),'pos']
        GetFisherVector.Fisher(tmp)
        MatchFunM.MatchFunM(tmp)
        GetMatchResult.GetMatchResult(tmp)
        result = GetMatchResult.GetBestResult(tmp)
        fi = open('pos_final.txt','a')
        s = '%s\t%s\t%d\t%s\t%s\n'%(result['video'], result['pano'], result['time'], result['lat'], result['lon'])
        fi.write(s)
        fi.close()
    f.close()
