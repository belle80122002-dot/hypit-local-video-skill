"""Optional light instrumental sketch; requires NumPy, uses no model or network."""
import argparse, math, wave
from pathlib import Path
import numpy as np

def compose(duration,output):
    if not math.isfinite(duration) or not 1 <= duration <= 600:
        raise ValueError('Choose a duration between 1 and 600 seconds')
    if output.exists():raise FileExistsError(output)
    sr=48000;n=round(duration*sr);music=np.zeros((n,2),dtype=np.float64);rng=np.random.default_rng(20260922)
    def note(start,midi,length,amp,pan=.5,bass=False):
        idx=round(start*sr);count=min(round(length*sr),n-idx)
        if count<=0:return
        t=np.arange(count)/sr;f=440*2**((midi-69)/12)
        env=(1-np.exp(-t*450))*np.exp(-t/(.24 if bass else .20))
        sig=(np.sin(2*np.pi*f*t)+(.22 if bass else .35)*np.sin(2*np.pi*f*2*t)+.13*np.sin(2*np.pi*f*3.01*t))*env*amp
        music[idx:idx+count,0]+=sig*math.sqrt(1-pan);music[idx:idx+count,1]+=sig*math.sqrt(pan)
    patterns=[[76,79,81,79,76,None,74,72],[76,79,84,None,83,79,76,None],[77,81,84,81,79,None,77,76],[74,79,83,None,81,79,74,None]]
    roots=[48,45,41,43]
    for bar in range(math.ceil(duration/2.4)):
        for step,midi in enumerate(patterns[bar%4]):
            if midi is not None:note(bar*2.4+step*.3,midi,.55,.13,.38 if step%2 else .62)
        for step in [0,2]:note(bar*2.4+step*.6,roots[bar%4],.50,.11,.5,True)
        for step in range(4):
            start=round((bar*2.4+step*.6)*sr);count=min(round(.06*sr),n-start)
            if count>0:
                noise=np.diff(rng.normal(0,1,count),prepend=0)*np.exp(-np.arange(count)/sr*85)*.009
                music[start:start+count]+=noise[:,None]
    times=np.arange(n)/sr
    fade=np.minimum(times/.18,1)*np.minimum(np.maximum(duration-times,0)/min(1.1,duration/2),1)
    music=np.clip(music*fade[:,None],-.95,.95)
    output.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(output),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((music*32767).astype('<i2').tobytes())
    print(f'Wrote {duration:.2f}s of instrumental audio: {output}')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--duration',type=float,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();compose(a.duration,a.output)