import Skeleton from "../common/Skeleton";


function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div>
        <Skeleton
          className="
            h-8 w-56
          "
        />

        <Skeleton
          className="
            mt-2 h-4 w-80
            max-w-full
          "
        />
      </div>

      <div
        className="
          grid gap-4
          sm:grid-cols-2
          lg:grid-cols-4
        "
      >
        {Array.from({
          length: 8,
        }).map(
          (_, index) => (
            <Skeleton
              key={index}
              className="h-32"
            />
          )
        )}
      </div>

      <Skeleton
        className="h-72"
      />
    </div>
  );
}


export default DashboardSkeleton;