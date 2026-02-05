/**
 * EmptyChartState Component
 *
 * Displays a friendly empty state when there's no data for charts.
 */

import React from "react";

interface EmptyChartStateProps {
  title?: string;
  description?: string;
}

export function EmptyChartState({
  title = "No data available",
  description = "Create some tasks to see analytics here",
}: EmptyChartStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[200px] p-8 text-center">
      <div className="mb-4">
        <svg
          className="w-16 h-16 text-gray-300 dark:text-gray-600"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          />
        </svg>
      </div>
      <h3 className="mb-2 text-lg font-semibold text-gray-700 dark:text-gray-300">
        {title}
      </h3>
      <p className="text-sm text-gray-500 dark:text-gray-400">{description}</p>
    </div>
  );
}
