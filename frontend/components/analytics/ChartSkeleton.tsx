/**
 * ChartSkeleton Component
 *
 * Loading skeleton for charts while data is being fetched.
 */

import React from "react";

export function ChartSkeleton() {
  return (
    <div className="animate-pulse space-y-4 p-4">
      {/* Chart title */}
      <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>

      {/* Chart area */}
      <div className="h-64 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-end justify-around p-4 space-x-2">
        {/* Simulated bars */}
        <div className="h-3/4 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
        <div className="h-1/2 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
        <div className="h-full bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
        <div className="h-2/3 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
        <div className="h-4/5 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
      </div>

      {/* Legend */}
      <div className="flex justify-center space-x-4">
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
      </div>
    </div>
  );
}
