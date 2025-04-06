import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faBullhorn, 
  faChevronRight, 
  faInfoCircle, 
  faArrowRight 
} from '@fortawesome/free-solid-svg-icons';

const AnnouncementsColumn = ({ announcements = [] }) => {
  // Safely transform announcements data
  const transformAnnouncements = () => {
    console.log('Raw announcements data:', announcements); // Debug log
  
    if (!Array.isArray(announcements)) {
      console.warn('Announcements is not an array:', announcements);
      return [];
    }
  
    return announcements
      .map(item => {
        try {
          console.log('Processing item:', item); // Debug log
          
          // Handle both Django REST format and normalized format
          const fields = item?.fields || item;
          
          // Debug field access
          console.log('Fields object:', fields);
          console.log('Title:', fields?.title);
          
          const processedItem = {
            id: item?.pk || item?.id || Math.random().toString(36).substr(2, 9),
            title: fields?.title || 'No title',
            message: fields?.message || '',
            created_at: fields?.created_at || new Date().toISOString(),
            is_active: fields?.is_active !== false
          };
          
          console.log('Processed item:', processedItem); // Debug log
          return processedItem;
        } catch (error) {
          console.error('Error processing announcement:', error, 'Item:', item);
          return null;
        }
      })
      .filter(Boolean);
  };

  // Get processed announcements
  const processedAnnouncements = transformAnnouncements()
    .filter(ann => ann.is_active)
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 3);


  return (
    <div className="announcements-column h-100">
      <div className="announcements-card h-100">
        <div className="announcements-header d-flex justify-content-between align-items-center">
          <h3 className="m-0">
            <FontAwesomeIcon icon={faBullhorn} className="me-2" />
            Latest Announcements
          </h3>
          <a href="#" className="view-all-link">
            View All <FontAwesomeIcon icon={faArrowRight} className="ms-1" />
          </a>
        </div>
        
        <div className="announcements-body d-flex flex-column justify-content-center">
          {processedAnnouncements.length > 0 ? (
            <div className="announcements-list">
              {processedAnnouncements.map((announcement) => (
                <div className="announcement-item" key={announcement.id}>
                  <div className="announcement-title">
                    <FontAwesomeIcon icon={faChevronRight} className="me-2 text-primary" />
                    {announcement.title}
                  </div>
                  <div className="announcement-content">
                    {announcement.message.length > 100 
                      ? `${announcement.message.substring(0, 100)}...` 
                      : announcement.message}
                  </div>
                  <div className="announcement-date text-muted small">
                    {new Date(announcement.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-announcements d-flex flex-column align-items-center justify-content-center">
              <FontAwesomeIcon 
                icon={faInfoCircle} 
                className="text-muted mb-2"
                size="2x"
              />
              <span className="text-muted">No current announcements</span>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .announcements-column {
          width: 100%;
          height: 100%;
        }
        
        .announcements-card {
          background-color: white;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.1);
          display: flex;
          flex-direction: column;
          border: 1px solid #e0e0e0;
          padding: 20px;
          height: 100%;
        }
        
        .announcements-header {
          padding-bottom: 15px;
          border-bottom: 1px solid #e0e0e0;
          margin-bottom: 15px;
        }
        
        .announcements-header h3 {
          margin: 0;
          font-size: 1.2rem;
          color: #2c3e50;
          font-weight: 600;
        }
        
        .announcements-body {
          flex-grow: 1;
          min-height: 0;
        }
        
        .announcements-list {
          display: flex;
          flex-direction: column;
          gap: 12px;
          height: 100%;
          overflow-y: auto;
          padding-right: 5px;
        }
        
        .announcement-item {
          padding: 12px;
          border-radius: 6px;
          transition: all 0.2s;
          border-left: 3px solid transparent;
          background-color: #f8f9fa;
        }
        
        .announcement-item:hover {
          background-color: #e9ecef;
          border-left: 3px solid #4ca1af;
        }
        
        .announcement-title {
          font-weight: 500;
          margin-bottom: 5px;
          color: #2c3e50;
        }
        
        .announcement-content {
          color: #6c757d;
          font-size: 0.9rem;
          line-height: 1.4;
          margin-bottom: 5px;
          white-space: pre-line;
        }
        
        .announcement-date {
          font-size: 0.8rem;
        }
        
        .no-announcements {
          height: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          color: #6c757d;
          text-align: center;
          padding: 20px 0;
        }
        
        .view-all-link {
          color: #4ca1af;
          text-decoration: none;
          font-weight: 500;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          transition: all 0.2s;
        }
        
        .view-all-link:hover {
          color: #3a7a8c;
          text-decoration: underline;
        }
      `}</style>
    </div>
  );
};

export default AnnouncementsColumn;