public class Main {

    public static void main(String[] args) throws InterruptedException {
        int branches = 3;
        int steps = 5;
        double initialPrice = 100.;
        ImitatedAsset ia = AssetGenerator.generateAssetByHistogram(10, branches, steps, 3, initialPrice);
//        System.out.println(ia);
//        System.out.println(BroadieGlassermanEstimation.upperEstimate(ia, 110));
//        System.out.println(BroadieGlassermanEstimation.lowerEstimate(ia, 110));
    }
}
