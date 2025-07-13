# Perceptual Urban Walk  

```mermaid
flowchart TD
    DP["download-panoramas"]
    click DP "./#download-panoramas"
    SI["segment-images"]
    click SI "./#segment-images"
    ES["extract-samples"]
    click ES "./#extract-samples"
    DP --> SI
    DP --> ES
```
#### [download-panoramas](./download-panoramas/)
#### [segment-images](./segment-images/)
#### [extract-samples](./extract-samples/)