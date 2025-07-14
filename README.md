# Perceptual Urban Walk  

```mermaid
flowchart TD
    DP["download-panoramas"]
    click DP "[1]"
    SI["segment-images"]
    ES["extract-samples"]
    DP --> SI
    DP --> ES
```
[1]: ./download-panoramas/  
2. [segment-images](./segment-images/)  
3. [extract-samples](./extract-samples/)  