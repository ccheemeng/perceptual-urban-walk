# Perceptual Urban Walk  

```mermaid
flowchart TD
    Boundary(["GeylangBahru-boundary.geojson"])
    Polygons(["GeylangBahru-polygons.geojson"])
    Buildings(["GeylangBahru-buildings.geojson"])
    Target(["GeylangBahru-target.csv"])
    Coords(["GeylangBahru-coords.csv"])
    Points(["GeylangBahru-points.csv"])
    Edges(["GeylangBahru-edges.csv"])
    Adjacencies(["GeylangBahru-adjacencies.json"])
    Samples(["GeylangBahru-samples.geojson"])
    Regions(["GeylangBahru-regions.geojson"])
    Clusters(["GeylangBahru-clusters.csv"])

    subgraph DP["download-panoramas"]
        DPPy["download_panoramas.py"]
        click DPPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/download-panoramas"
    end
    subgraph SI["segment-images"]
        SIPy["segment_images.py"]
        click SIPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/segment-images"
    end
    subgraph ES["extract-samples"]
        GRPy["generate_roads.py"]
        ESPy["extract_samples.py"]
        click GRPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/extract-samples"
        click ESPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/extract-samples"
    end
    subgraph GP["generate-pc"]
        PSPy["project_segmentations.py"]
        GSPPy["generate_sample_pc.py"]
        CoSPy["compile_samples.py"]
        click PSPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/generate-pc"
        click GSPPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/generate-pc"
        click CoSPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/generate-pc"
    end
    subgraph EP["encode-pc"]
        subgraph LPNAE["labelled-pointnet-autoencoder"]
        end
        EPPy["encode-pc.py"]
        BMSD(["best-model-state-dict.pt"])
        click LPNAE href "https://github.com/ccheemeng/labelled-pointnet-autoencoder/tree/main"
        click EPPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/encode-pc"
        click BMSD href "https://github.com/ccheemeng/labelled-pointnet-autoencoder/releases/tag/v0.1.1"
    end
    subgraph CS["cluster-samples"]
        ClSPy["cluster_samples.py"]
        click ClSPy href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/cluster-samples"
    end
    subgraph GE["generate-env"]
        subgraph PEG["perceptual-env-gen"]
            PEGMain["Main.py"]
            PEGGenerate["Generate.py"]
        end
        subgraph QuerySamplePcs["beautyworld-sample-pc"]
            QuerySamplePc(["x_y.csv"])
        end
        GESh["generate_env.sh"]
        GEPSh["generate_env_pc.sh"]
        click PEG href "https://github.com/ccheemeng/perceptual-env-gen/tree/main"
        click GESh href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/generate-env"
        click GEPSh href "https://github.com/ccheemeng/perceptual-urban-walk/tree/main/generate-env"
    end

    subgraph Panos["GeylangBahru-panos"]
        Pano(["id.jpg"])
    end
    subgraph Segmentations["GeylangBahru-segmented"]
        Segmentation(["id.json"])
    end
    subgraph SegmentationVizs["GeylangBahru-segmented-visualised"]
        SegmentationViz(["id.jpg"])
    end
    subgraph SamplePoints["GeylangBahru-sample-points"]
        SamplePoint(["x_y.csv"])
    end
    subgraph SampleRegions["GeylangBahru-sample-regions"]
        SampleRegion(["x_y.geojson"])
    end
    subgraph SegmentedPcs["GeylangBahru-segmented-pc"]
        SegmentedPc(["id.csv"])
    end
    subgraph SamplePcs["GeylangBahru-sample-pc"]
        SamplePc(["x_y.csv"])
    end
    subgraph Encodings["GeylangBahru-encodings"]
        Encoding(["x_y.json"])
    end
    subgraph EnvGen["GeylangBahru-env-gen"]
        subgraph PolygonGen["polygonID"]
            AttributesGen["attributes.csv"]
            BuildingsGen["buildings.geojson"]
            PerceptionsGen["perceptions.csv"]
            PointsGen["points.csv"]
            PolygonsGen["polygons.geojson"]
            SamplesGen["samples.csv"]
        end
    end

    Boundary --> DPPy
    DPPy --> Panos
    DPPy --> Coords
    Panos --> SIPy
    SIPy --> Segmentations
    SIPy --> SegmentationVizs
    Coords --> GRPy
    GRPy --> Points
    GRPy --> Edges
    GRPy --> Adjacencies
    Points --> ESPy
    Adjacencies --> ESPy
    Boundary --> ESPy
    ESPy --> SamplePoints
    ESPy --> SampleRegions
    Coords --> PSPy
    Segmentations --> PSPy
    Buildings --> PSPy
    PSPy --> SegmentedPcs
    SamplePoints --> GSPPy
    SampleRegions --> GSPPy
    SegmentedPcs --> GSPPy
    GSPPy --> SamplePcs
    SamplePcs --> CoSPy
    SampleRegions --> CoSPy
    CoSPy --> Samples
    CoSPy --> Regions
    LPNAE --o BMSD
    LPNAE --- EPPy
    SamplePcs --> EPPy
    BMSD --> EPPy
    EPPy --> Encodings
    Encodings --> ClSPy
    ClSPy --> Clusters
    GESh --- PEGMain
    GEPSh --- PEGGenerate
    Samples --> PEGMain
    Regions --> PEGMain
    Clusters --> PEGMain
    Polygons --> PEGMain
    Target --> PEGMain
    PEGMain --> AttributesGen
    PEGMain --> BuildingsGen
    PEGMain --> PerceptionsGen
    PEGMain --> PolygonsGen
    PEGMain --> SamplesGen
    PEG --o QuerySamplePcs
    PerceptionsGen --> PEGGenerate
    PolygonsGen --> PEGGenerate
    QuerySamplePcs --> PEGGenerate
    PEGGenerate --> PointsGen

    style Panos rx:0.75vw,ry:0.75vw
    style Segmentations rx:0.75vw,ry:0.75vw
    style SegmentationVizs rx:0.75vw,ry:0.75vw
    style SamplePoints rx:0.75vw,ry:0.75vw
    style SampleRegions rx:0.75vw,ry:0.75vw
    style SegmentedPcs rx:0.75vw,ry:0.75vw
    style SamplePcs rx:0.75vw,ry:0.75vw
    style Encodings rx:0.75vw,ry:0.75vw
    style EnvGen rx:0.75vw,ry:0.75vw
    style PolygonGen rx:0.75vw,ry:0.75vw
```