'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Text, Button } from '@radix-ui/themes';
import navigationConfig from '@/config/navigation.json';

interface NavigationItem {
  id: string;
  label: string;
  href?: string;
  icon: string;
  children?: NavigationItem[];
}

interface SidebarProps {
  className?: string;
}

export function Sidebar({ className }: SidebarProps) {
  const pathname = usePathname();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggleExpanded = (itemId: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(itemId)) {
      newExpanded.delete(itemId);
    } else {
      newExpanded.add(itemId);
    }
    setExpandedItems(newExpanded);
  };

  const isActive = (href?: string) => {
    if (!href) return false;
    return pathname === href || pathname.startsWith(href + '/');
  };

  const renderNavigationItem = (item: NavigationItem, level = 0) => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.has(item.id);
    const active = isActive(item.href);

    return (
      <div key={item.id} className="w-full">
        <div
          className={`flex items-center justify-between w-full px-3 py-2 rounded-md transition-colors ${
            active ? 'bg-yellow-100 text-yellow-900' : 'text-gray-700 hover:bg-gray-100'
          } ${level > 0 ? 'ml-4' : ''}`}
        >
          {item.href ? (
            <Link href={item.href} className="flex items-center flex-1">
              <Text size="2" weight={active ? 'medium' : 'regular'}>
                {item.label}
              </Text>
            </Link>
          ) : (
            <div className="flex items-center flex-1">
              <Text size="2" weight="medium">
                {item.label}
              </Text>
            </div>
          )}

          {hasChildren && (
            <Button
              variant="ghost"
              size="1"
              onClick={() => toggleExpanded(item.id)}
              className="ml-2 p-1"
            >
              <Text size="1">{isExpanded ? '−' : '+'}</Text>
            </Button>
          )}
        </div>

        {hasChildren && isExpanded && (
          <div className="mt-1 space-y-1">
            {item.children?.map(child => renderNavigationItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <aside className={`w-64 bg-white border-r border-gray-200 h-full ${className || ''}`}>
      <div className="p-4">
        <nav className="space-y-2">
          {navigationConfig.navigation.map(item => renderNavigationItem(item))}
        </nav>
      </div>
    </aside>
  );
}

export default Sidebar;
