'use client';

import React from "react";
import { Command as CommandPrimitive } from "cmdk";
import { Dialog, DialogContent } from '@/components/ui/dialog';
import { useRouter } from 'next/navigation';
import { LayoutDashboard, ListTodo, ShoppingCart, FileText, Calendar } from 'lucide-react'; // Import Lucide icons

export function CommandSearch() {
  const [open, setOpen] = React.useState(false);
  const [search, setSearch] = React.useState('');
  const router = useRouter();

  // Dummy data for navigation and tasks
  const navItems = [
    { value: 'dashboard', label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { value: 'tasks', label: 'Tasks', href: '/tasks', icon: ListTodo },
  ];

  const dummyTasks = [
    { value: 'buy-groceries', label: 'Buy groceries', href: '/tasks/1', icon: ShoppingCart },
    { value: 'finish-report', label: 'Finish report', href: '/tasks/2', icon: FileText },
    { value: 'schedule-meeting', label: 'Schedule meeting', href: '/tasks/3', icon: Calendar },
  ];

  const filteredNavItems = navItems.filter(item =>
    item.label.toLowerCase().includes(search.toLowerCase())
  );

  const filteredTasks = dummyTasks.filter(item =>
    item.label.toLowerCase().includes(search.toLowerCase())
  );

  const handleSelect = (href: string) => {
    router.push(href);
    setOpen(false);
  };

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="p-0 overflow-hidden shadow-lg border-none">
        <CommandPrimitive className="h-full w-full flex flex-col">
          <CommandPrimitive.Input
            placeholder="Type a command or search..."
            value={search}
            onValueChange={setSearch}
            className="flex h-12 w-full rounded-md bg-transparent py-3 px-4 text-sm outline-none placeholder:text-gray-500 disabled:cursor-not-allowed disabled:opacity-50 dark:placeholder:text-gray-400"
          />
          <CommandPrimitive.List className="overflow-y-auto overflow-x-hidden p-2">
            <CommandPrimitive.Empty>No results found.</CommandPrimitive.Empty>

            {filteredNavItems.length > 0 && (
              <CommandPrimitive.Group heading="Navigation">
                {filteredNavItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <CommandPrimitive.Item key={item.value} onSelect={() => handleSelect(item.href)} className="flex items-center space-x-2">
                      <Icon className="h-4 w-4" />
                      <span>{item.label}</span>
                    </CommandPrimitive.Item>
                  );
                })}
              </CommandPrimitive.Group>
            )}

            {filteredTasks.length > 0 && (
              <CommandPrimitive.Group heading="Tasks">
                {filteredTasks.map((item) => {
                  const Icon = item.icon;
                  return (
                    <CommandPrimitive.Item key={item.value} onSelect={() => handleSelect(item.href)} className="flex items-center space-x-2">
                      <Icon className="h-4 w-4" />
                      <span>{item.label}</span>
                    </CommandPrimitive.Item>
                  );
                })}
              </CommandPrimitive.Group>
            )}
          </CommandPrimitive.List>
        </CommandPrimitive>
      </DialogContent>
    </Dialog>
  );
}